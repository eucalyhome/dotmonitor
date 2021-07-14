# LED STATUS OUTPUT MOCKUP

By eucalyptus. 2021.

## 環境
- Python3 系列
- pillowライブラリ

## 動作確認
### モンスター行進
`
python3 dotmonitor.py
`
- モンスター描画関数、背景描画関数に、0-100のパラメータを与えることで、背景色、モンスター数、モンスター速度を制御できます
- 画面描画文字は固定です


### ステータスモニタ
`
python3 statusmonitor.py
`
- ステータス表示には、別途LibreHardwareMonitorを動作の上、httpにてjson取得が必要です
- デモ用に、開発環境のデータを、「data.json」として添付してあります

### 留意事項
- デモ動作には、GUI環境が必要です (標準tkライブラリ)

### 同梱データ著作権
- ドット絵: ヌー@ドット絵素材置き場 ( http://damagedgold.wp.xdomain.jp/ )
- フォント: ピクセルエムプラス ( https://itouhiro.hatenablog.com/entry/20130602/font )
