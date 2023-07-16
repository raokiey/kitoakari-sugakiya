# 【非公式】鬼頭明里のスガキヤだがや！ コラボ店舗マップ
鬼頭明里さんとスガキヤさんのコラボ企画である「[鬼頭明里のスガキヤだがや！](https://sugakiya-campaign.net/sugakiyadagaya/)」の対象店舗を個人が地図に可視化したものです。  
## アプリ
[こちら](https://kitoakari-sugakiya-mymap.streamlit.app/)から閲覧することができます。

https://github.com/raokiey/kitoakari-sugakiya/assets/56877037/1963fcf9-e5d6-4320-860d-372a90dbb4da

## 仕組み
1. コラボ店舗である253店舗の情報を頑張ってCSV形式でまとめる  
2. 店舗名や住所からをGoogle Apps Script（以下GAS）を用いてジオコーディングを行い、緯度経度を得る  
3. 2.で作成したCSVの情報にコラボグッズ販売情報などを加える  
4. スガキヤさん公式ツイートからコラボグッズの情報のみIFFTを用いて取得し、Google Drive上にCSV形式で保存する  
5. 4.の情報を用いて2.で作成したCSV形式の情報をGASを用いて定期的に更新する
6. 5.で作成されるCSVをPandasを用いて読み込み、FoliumおよびStreamlitを用いて地図上に可視化し、Webでアクセスできるようにする
