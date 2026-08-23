# 画像置き場(通信 第2回:LoRa無線モジュールを使ってみる)

`09_LoRa無線モジュールを使ってみる.md` で使用する画像です。

## 配置済み(そのまま使えます)

- `00_lora_module_photo.jpg` — LoRaモジュール E220-900T22S(JP)の実物写真(表・裏・ピン配置)。[DRAGON TORCH(株式会社クレアリンクテクノロジー)公式サイト](https://dragon-torch.tech/rf-modules/lora/e220-900t22s-jp-r2/)よりダウンロードして自己ホスト。本文にクレジット表記あり
- `01_lesson_thumbnail.svg` — 今日のゴール(有線→LoRaを挟む→同じ挙動、最後にLED遠隔操作)の全体図。自作
- `02_wiring.svg` — Pico W ⇔ LoRaモジュールの配線図(TX/RXクロス、M0/M1→GND、アンテナ注意)。自作
- `03_modulation_demodulation.svg` — LoRaモジュールの変調・復調の役割を示す図。自作
- `04_packet_header.svg` — 通常送信モードのデータ形式(ADDH+ADDL+CHAN+ペイロード)を示す図。自作
- `05_duty_cycle.svg` — 電波法の送信休止時間(送信時間の10倍以上)を示す図。自作

## 未取得(当日撮影して差し替えてください)

- `06_lora_result.png`(3節:LoRa経由での送受信結果、配線の様子)
- `07_remote_led_result.png`(6節:タクトスイッチでLEDを遠隔操作している様子)
- `08_challenge_result.png`(8節:確認課題の実施結果)
