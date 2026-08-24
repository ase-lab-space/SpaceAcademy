# 画像置き場(通信 第2回:LoRa無線モジュールを使ってみる)

`09_LoRa無線モジュールを使ってみる.md` で使用する画像です。

## 配置済み(そのまま使えます)

- `00_lora_module_photo.jpg` — LoRaモジュール E220-900T22S(JP)の実物写真(表・裏・ピン配置)。[DRAGON TORCH(株式会社クレアリンクテクノロジー)公式サイト](https://dragon-torch.tech/rf-modules/lora/e220-900t22s-jp-r2/)よりダウンロードして自己ホスト。本文にクレジット表記あり
- `01_lesson_thumbnail.svg` — 今日のゴール(有線→LoRaを挟む→同じ挙動、最後にLED遠隔操作)の全体図。自作
- `02_wiring.svg` — Pico W ⇔ LoRaモジュールの配線図(TX/RXクロス、AUX→GP14、M0/M1→GND、アンテナ注意)。自作
- `02b_breadboard_fritzing.svg` — 同じ配線を、ブレッドボード上の実体配線図(Fritzing風)として表したもの。**実際のFritzingソフトウェアの出力ではなく、同じ見た目になるよう自作したもの**。本物のFritzing図に差し替えたい場合はこのファイルを置き換えてください
- `03_modulation_demodulation.svg` — LoRaモジュールの変調・復調の役割を示す図。自作
- `04_packet_header.svg` — 通常送信モードのデータ形式(ADDH+ADDL+CHAN+ペイロード)を示す図。自作
- `05_duty_cycle.svg` — 電波法の送信休止時間(送信の10倍以上休止)を示す図。自作
- `06_aux_states.svg` — AUXピンのHIGH/LOW状態と、送信時のタイムラインを示す図。自作

## 未取得(当日撮影して差し替えてください)

- `07_lora_result.png`(3.3節:LoRa経由での送受信結果、配線の様子)
- `07b_aux_plotter_result.png`(6.1節:PlotterでAUXの波形が観察できている様子)
- `08_remote_led_result.png`(7節:タクトスイッチでLEDを遠隔操作している様子)
- `09_challenge_result.png`(9節:確認課題の実施結果)
- `10_rssi_distance_result.png`(9節・発展課題:屋外でRSSIを測定している様子、および距離とRSSIの関係を示す表・グラフ)
