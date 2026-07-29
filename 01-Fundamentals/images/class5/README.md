# 画像置き場(電子工作 第3回:UART通信)

`06_UARTでマイコン同士を通信させる.md` で使用する画像です。

## 配置済み(そのまま使えます・すべて自作)

- `00_lesson_thumbnail.svg` — 冒頭のゴール提示用サムネイル。2台のPico Wが"PING"を送り合う様子
- `01_uart_frame_waveform.png` — UARTのフレーム波形図(スタート/データ8bit/ストップビット)。`gen_uart_frame.py`(matplotlib)で生成。文字'A'(0x41)をLSBファーストで送る例
- `02_uart_topology.svg` — TX/RXクロス配線・GND共有の概念図
- `03_async_analogy.svg` — スタートビット(せーの)+ボーレート(同じテンポ)で同期する非同期通信のたとえ図。I2C/SPIに触れずに理解できる説明にした
- `04_serial_vs_parallel.svg` — シリアル通信とパラレル通信の違いの比較図
- `05_clock_drift_and_midbit_sampling.svg` — クロックのわずかな速度差がフレーム後半で誤読リスクになること、UARTがビット中央でサンプリングして対策していることの図。**本編には掲載せず、宿題(問い2)の指導者用解答(`instructor-notes/06_解答.md`)専用**として使用(答えを直接示す図のため、学生向け本文には出さない方針)
- `gen_uart_frame.py` — `01_uart_frame_waveform.png`を生成したPythonスクリプト。再実行・改変可能

## 未取得(当日撮影して差し替えてください)

- `06_dual_board_power_setup.jpg`(ボードAをモバイルバッテリー等につなぎ、ボードBをPCにつないで観察している様子)
- `07_uart_send_receive_result.png`(ボードBのThonnyシェルに受信ログが流れている様子)
- `08_baudrate_mismatch_garbled.png`(ボーレート不一致で文字化けした受信結果)
- `09_challenge_result.jpg`(確認課題:UART経由でLED/モーターが反応する様子、または1byteの壁でエラーが出た様子)
