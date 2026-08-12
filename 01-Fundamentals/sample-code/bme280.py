# ============================================================
# BME280(温湿度・気圧センサ)用ドライバ — SpaceAcademy 電子工作 第4回
# ============================================================
#
# このファイルの目的:
#   「ライブラリの中で、実際にレジスタを叩いて値を取り出す処理が
#   どうなっているか」を、読めばそのまま追えるようにすることです。
#   市販のライブラリのようにブラックボックス化せず、あえて薄く・
#   素直に書いています(速度やエラー処理の完全性より、読みやすさを優先)。
#
# 使い方(CanSat_Fundamentalsと同じスタイルです):
#
#   I2Cの場合
#   ---------
#     from machine import I2C, Pin
#     import bme280
#
#     i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=100_000)
#     bme = bme280.BME280(i2c=i2c)        # SDOをGNDに接続時。VDD接続時は address=0x77
#     print(bme.values)                    # (気温[℃], 気圧[hPa], 湿度[%])
#
#   SPIの場合
#   ---------
#     from machine import SPI, Pin
#     import bme280
#
#     cs = Pin(17, Pin.OUT)
#     spi = SPI(0, baudrate=1_000_000, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
#     bme = bme280.BME280(spi=spi, cs=cs)
#     print(bme.values)
#
# ============================================================

import time

# ---- レジスタアドレス(データシート Table 18: Memory map より) ----
# 06_I2CとSPIでセンサと話す.md の「4.2 レジスタマップとデータシートの対応」
# で見た表と、番地が一致しているか見比べてみてください。
_REG_ID = 0xD0
_REG_CTRL_HUM = 0xF2
_REG_CTRL_MEAS = 0xF4
_REG_PRESS_MSB = 0xF7  # ここから8byte連続で press/temp/hum の msb・lsb・xlsb が並んでいる
_REG_CALIB_00 = 0x88  # 気温・気圧の校正値(26byte)
_REG_CALIB_26 = 0xE1  # 湿度の校正値(7byte)

_CHIP_ID = 0x60  # idレジスタの固定値。4.3節で自分の手で読んだ値と同じもの


class BME280:
    """BME280センサのドライバ。

    `i2c=` を渡せばI2Cモード、`spi=`(と`cs=`)を渡せばSPIモードで動きます。
    内部でやっていることはどちらのモードでも同じで、「レジスタを読み書き
    する方法(_I2CBus / _SPIBus)」だけが違います。
    """

    def __init__(self, i2c=None, address=0x76, spi=None, cs=None):
        if i2c is not None:
            self._bus = _I2CBus(i2c, address)
        elif spi is not None:
            if cs is None:
                raise ValueError("SPIモードではcs(チップセレクト用Pin)も指定してください")
            self._bus = _SPIBus(spi, cs)
        else:
            raise ValueError("i2c= か、spi=とcs=のどちらかを指定してください")

        # まずIDレジスタを読み、本当にBME280につながっているか確認する。
        # ここが4.3節で手動でやった「IDレジスタを直接読んでみる」と同じ処理。
        chip_id = self._bus.read_register(_REG_ID)
        if chip_id != _CHIP_ID:
            raise RuntimeError(
                "BME280が見つかりません(idレジスタ = 0x{:02X}、期待値は0x{:02X})。"
                "配線とアドレス/CS設定を確認してください。".format(chip_id, _CHIP_ID)
            )

        self._load_calibration()
        self._configure_measurement()
        self._t_fine = 0  # 気圧・湿度の補正計算で使う中間値(compensate_*で更新される)

    # ------------------------------------------------------------
    # 初期設定
    # ------------------------------------------------------------

    def _configure_measurement(self):
        """センサに「測定を始めてください」と設定を書き込む。"""
        # ctrl_hum: 湿度のオーバーサンプリングを x1 に設定
        self._bus.write_register(_REG_CTRL_HUM, 0x01)
        # ctrl_meas: 気温・気圧のオーバーサンプリングをx1にし、
        #            測定モードを「ノーマルモード(=繰り返し自動測定)」にする
        self._bus.write_register(_REG_CTRL_MEAS, 0x27)
        time.sleep_ms(10)  # 設定が反映されるまで少し待つ

    def _load_calibration(self):
        """センサ固有の「補正係数(校正値)」を読み込む。

        BME280は、工場出荷時に個体ごとの補正係数があらかじめレジスタに
        書き込まれています。生の測定値(raw)は、この係数を使って計算しないと
        正しい温度・気圧・湿度になりません(4.2節で見た通り、レジスタの値は
        あくまで「生のビット列」でしかないためです)。
        """
        calib = self._bus.read_registers(_REG_CALIB_00, 26)
        h_calib = self._bus.read_registers(_REG_CALIB_26, 7)

        # 気温用の係数(温度の補正はこの3つだけで完結する)
        self._dig_T1 = _read_u16(calib, 0)
        self._dig_T2 = _read_s16(calib, 2)
        self._dig_T3 = _read_s16(calib, 4)

        # 気圧用の係数
        self._dig_P1 = _read_u16(calib, 6)
        self._dig_P2 = _read_s16(calib, 8)
        self._dig_P3 = _read_s16(calib, 10)
        self._dig_P4 = _read_s16(calib, 12)
        self._dig_P5 = _read_s16(calib, 14)
        self._dig_P6 = _read_s16(calib, 16)
        self._dig_P7 = _read_s16(calib, 18)
        self._dig_P8 = _read_s16(calib, 20)
        self._dig_P9 = _read_s16(calib, 22)

        # 湿度用の係数。dig_H4とdig_H5だけ、2つのレジスタの一部ずつを
        # 組み合わせて作る変わった形をしている(データシート4.2.2節)。
        # これも「複数レジスタから1つの値を組み立てる」ビットシフトの一例。
        self._dig_H1 = calib[25]
        self._dig_H2 = _read_s16(h_calib, 0)
        self._dig_H3 = h_calib[2]
        e4, e5, e6 = h_calib[3], h_calib[4], h_calib[5]
        self._dig_H4 = _to_signed((e4 << 4) | (e5 & 0x0F), 12)
        self._dig_H5 = _to_signed((e6 << 4) | (e5 >> 4), 12)
        self._dig_H6 = _to_signed(h_calib[6], 8)

    # ------------------------------------------------------------
    # 測定値の取得
    # ------------------------------------------------------------

    def _read_raw(self):
        """press_msb(0xF7)から8byte連続で読み、3つの生の値に組み立てる。

        06_I2CとSPIでセンサと話す.md の図(11_bit_shift_assembly.svg)と
        まったく同じビットシフトを、ここで実際に行っています。
        """
        data = self._bus.read_registers(_REG_PRESS_MSB, 8)

        raw_press = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        raw_temp = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
        raw_hum = (data[6] << 8) | data[7]

        return raw_temp, raw_press, raw_hum

    def _compensate_temperature(self, raw_temp):
        # Bosch公式データシート(4.2.3節)の補正式をそのまま実装したもの。
        # 数式自体を覚える必要はありません。「生の値+校正係数 → 本当の気温」
        # という変換をしている、とだけ分かれば十分です。
        var1 = (raw_temp / 16384.0 - self._dig_T1 / 1024.0) * self._dig_T2
        var2 = (raw_temp / 131072.0 - self._dig_T1 / 8192.0) ** 2 * self._dig_T3
        self._t_fine = var1 + var2  # 気圧・湿度の計算でも使う値なので保存しておく
        return (var1 + var2) / 5120.0

    def _compensate_pressure(self, raw_press):
        # こちらもBosch公式の補正式(4.2.3節)。気温の補正結果(t_fine)を使う。
        var1 = self._t_fine / 2.0 - 64000.0
        var2 = var1 * var1 * self._dig_P6 / 32768.0
        var2 = var2 + var1 * self._dig_P5 * 2.0
        var2 = var2 / 4.0 + self._dig_P4 * 65536.0
        var1 = (self._dig_P3 * var1 * var1 / 524288.0 + self._dig_P2 * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * self._dig_P1
        if var1 == 0:
            return 0.0  # ゼロ除算を避ける(データシート記載の注意点)
        pressure = 1048576.0 - raw_press
        pressure = (pressure - var2 / 4096.0) * 6250.0 / var1
        var1 = self._dig_P9 * pressure * pressure / 2147483648.0
        var2 = pressure * self._dig_P8 / 32768.0
        pressure = pressure + (var1 + var2 + self._dig_P7) / 16.0
        return pressure / 100.0  # Pa -> hPa

    def _compensate_humidity(self, raw_hum):
        # Bosch公式の補正式(4.2.3節)。変数名var1〜var5もデータシートの表記に合わせた。
        var1 = self._t_fine - 76800.0
        var2 = self._dig_H4 * 64.0 + (self._dig_H5 / 16384.0) * var1
        var3 = raw_hum - var2
        var4 = self._dig_H2 / 65536.0
        var5 = 1.0 + (self._dig_H3 / 67108864.0) * var1
        var5 = 1.0 + (self._dig_H6 / 67108864.0) * var1 * var5
        var5 = var3 * var4 * var5
        humidity = var5 * (1.0 - self._dig_H1 * var5 / 524288.0)
        if humidity > 100.0:
            humidity = 100.0
        elif humidity < 0.0:
            humidity = 0.0
        return humidity

    @property
    def values(self):
        """(気温[℃], 気圧[hPa], 湿度[%])のタプルを返す。

        06のコード例では毎回これを呼んでいます。呼ばれるたびに、
        (1)レジスタを読む → (2)ビットシフトで組み立てる → (3)校正係数で補正する
        という3ステップを、このメソッドの中で毎回やり直しています。
        """
        raw_temp, raw_press, raw_hum = self._read_raw()
        temperature = self._compensate_temperature(raw_temp)
        pressure = self._compensate_pressure(raw_press)
        humidity = self._compensate_humidity(raw_hum)
        return (round(temperature, 2), round(pressure, 2), round(humidity, 2))


# ------------------------------------------------------------
# バイト列 → 整数への変換ヘルパー
# ------------------------------------------------------------

def _read_u16(data, offset):
    """dataのoffset番目から2byteを、符号なし16bit整数として読む(リトルエンディアン)。"""
    return data[offset] | (data[offset + 1] << 8)


def _read_s16(data, offset):
    """dataのoffset番目から2byteを、符号あり16bit整数として読む。"""
    return _to_signed(_read_u16(data, offset), 16)


def _to_signed(value, bits):
    """符号なし整数を、bits幅の符号あり整数(2の補数)として解釈し直す。"""
    if value & (1 << (bits - 1)):
        value -= 1 << bits
    return value


# ------------------------------------------------------------
# レジスタの読み書き方法(I2C版 / SPI版)
# ------------------------------------------------------------
#
# BME280クラスの本体(補正計算など)はI2C/SPIどちらでも共通です。
# 違うのは「レジスタをどう読み書きするか」だけなので、その部分だけを
# 下の2つのクラスに切り出しています。BME280クラスからは
# `self._bus.read_register(...)` のように、プロトコルの違いを意識せず
# 呼び出せるようにしてあります。

class _I2CBus:
    """I2Cでレジスタを読み書きする。"""

    def __init__(self, i2c, address):
        self._i2c = i2c
        self._addr = address

    def read_register(self, register):
        return self._i2c.readfrom_mem(self._addr, register, 1)[0]

    def read_registers(self, register, length):
        return self._i2c.readfrom_mem(self._addr, register, length)

    def write_register(self, register, value):
        self._i2c.writeto_mem(self._addr, register, bytes([value]))


class _SPIBus:
    """SPIでレジスタを読み書きする。

    06_I2CとSPIでセンサと話す.md の「4.3 手を動かして確かめる」で
    書いたコード(`0xD0 | 0x80` でIDレジスタを読む処理)と、まったく
    同じ考え方をそのままクラスにしたものです。
    """

    _READ_BIT = 0x80  # このビットを立てて送ると「読み取り」の合図になる

    def __init__(self, spi, cs):
        self._spi = spi
        self._cs = cs
        self._cs.value(1)  # 最初は未選択の状態にしておく

    def read_register(self, register):
        return self.read_registers(register, 1)[0]

    def read_registers(self, register, length):
        self._cs.value(0)  # センサを選択
        self._spi.write(bytes([register | self._READ_BIT]))  # 読み取りたい番地を指定
        data = self._spi.read(length)  # 指定したbyte数だけ受け取る
        self._cs.value(1)  # 選択解除
        return data

    def write_register(self, register, value):
        self._cs.value(0)
        # 書き込み時はbit7を立てない(0x7Fでマスクして消す)
        self._spi.write(bytes([register & 0x7F, value]))
        self._cs.value(1)
