# 画像置き場(電子工作 第4回:I2CとSPIでセンサと話す)

`06_I2CとSPIでセンサと話す.md` で使用する画像です。

## 配置済み(そのまま使えます)

- `00_lesson_thumbnail.svg` — 冒頭のゴール提示用サムネイル。自作
- `01_bme280_photo.jpg` — BME280実物写真。CanSat_Fundamentals(`teach_02_Hardware/91-images/BME280.jpg`)から流用
- `02_spi_wiring.svg` — SPI配線図(Pico W ⇔ BME280)。自作
- `03_spi_protocol.svg` — SPI通信のタイミングイメージ図。自作
- `05_i2c_wiring.jpg` — I2C配線図。CanSat_Fundamentals(`teach_02_Hardware/91-images/センサを使ってみよう.jpg`)から流用。センサモジュールの見た目は今回のAE-BME280と少し異なるが、SDA/SCL配線パターンは共通なので使用可(本文に注記あり)
- `06_i2c_protocol.svg` — I2C通信のアドレス・ACKイメージ図。自作
- `10_bme280_datasheet_memorymap.png` — **Bosch純正のBME280データシート(BST-BME280-DS001-23)** p.27「Table 18: Memory map」を切り出したもの(公式PDFを取得し、PyMuPDFでページをレンダリング後トリミング)。「実際のデータシートはこんな感じ」という耐性をつける目的で使用。※AE-BME280(秋月電子モジュール)のマニュアル版は表が回転して読みにくいため不採用
- `11_bit_shift_assembly.svg` — 3つのレジスタ(temp_msb/lsb/xlsb)からビットシフトで1つの値を組み立てる様子の直感図。自作。社内スライド資料「マイコン編.pdf」p.49のレイアウト(空のビットマス+シフト矢印+組み立て後の枠)を参考にデザインを揃えた。p.50のコード表現は今回意図的に含めていない
- `12_spi_topology_ref.svg` — CanSat_Fundamentals(`teach_02_Hardware/02_センサの信号.md`)で参照されているSPIトポロジー図(Analog Devices "Introduction to SPI Interface"由来)。直リンク先(analog.com)が本環境から接続不可だったため、Wayback Machine経由で取得しダウンロード・自己ホスト
- `13_i2c_topology_ref.png` — 同じくCanSat_Fundamentalsで参照されているI2Cトポロジー図(macnica.co.jp由来)。ダウンロードして自己ホスト

## 未取得(当日撮影して差し替えてください)

- `07_spi_result.png`(SPIで気温・気圧・湿度が表示された結果)
- `08_i2c_result.png`(I2Cで気温・気圧・湿度が表示された結果)
- `09_challenge_result.png`(確認課題の実施結果)
- `14_sensor_noise_stats.png`(Plotterのグラフ+平均値・分散・標準偏差の出力結果)
