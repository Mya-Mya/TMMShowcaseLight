# TMMShowcaseLight
教材メディア(Teachin Material Media)の展示Webアプリです。

CSVファイルを用いて展示する教材メディアのデータを作れば、自動的にHTML及びJS形式のWebアプリを生成することができます。

# 初心者向け : Webアプリの作り方
## 用意すべきもの
* npm
* python3系
* CSVエディタ : Excelでは正常に開けないCSVファイルを扱うため、その他のソフトを使って下さい。例えば[Cassava](https://www.asukaze.net/soft/cassava/)などがおすすめです。

## 1. 教材メディアの構造を知る。
教材メディアには階層が存在します。それは以下の通りです。

`シェルフ > レッスン > チャプター > メディア`

* メディア : `リチウムの炎色反応の動画`等の、1つのメディアを表すものです。今対応しているものでは、1本のYouTube動画があります。今後需要によってはその他の形式のメディアも対応したいと思っています。
* チャプター : 複数のメディアを束ねたものです。
例えば授業中、`1.リチウムの炎色反応の動画 2.ナトリウムの炎色反応の動画 3.ホウ素の炎色反応の動画` といったように、生徒さんに見て欲しいメディアが連続して3つある場合は、
`炎色反応`というチャプターの下、これら3つのメディアをまとめます。
* レッスン : `化学の授業第3回目`等の、1回の授業を表す存在です。1回の授業で、このレッスン下にあるチャプター全てを使います。
* シェルフ : `化学の教科書 上`等の、複数のレッスンを束ねたものです。一連の教材シリーズ、1冊の教科書、1冊の本の中での大きな区切りなどを表します。

## 2. 教材メディアのデータファイルを作る。
データはカンマ区切り、**UTF-8エンコーディングの**CSVファイルで記述します。
ExcelはUTF-8エンコーディングのCSVファイルを開けないため、別のソフトで作業する必要があります。
Google Spreadsheet でデータを作り、[ファイル]>[ダウンロード]>[カンマ区切りの値]の順番でダウンロードするのもよいかと思います。

例えば教材メディアを以下のように配置したいとします。
- シェルフ1
  - レッスン1
    - チャプター1
      - YouTube動画 youtu.be/vvvvv
      - YouTube動画 youtu.be/wwwww
    - チャプター2
      - YouTube動画 youtu.be/xxxxx
  - レッスン2
    - チャプター3
      - YouTube動画 youtu.be/yyyyyy
- シェルフ1
  - レッスン1
    - チャプター1
      - YouTube動画 youtu.be/zzzzzz

この際には、本リポジトリ内にある[TMMData_example_tmvf2d.csv](https://github.com/Mya-Mya/TMMShowcaseLight/blob/main/TMMData_example_tmvf2d.csv)のように書きます。

### メディアタイプとメディアペイロードの書き方
1本のYouTube動画をメディアとして展示したい場合、以下のように書きます。
* メディアタイプ : `youtube`
* メディアペイロード
  * 通常は、`<YouTube動画のID>`
  * 再生位置を`t`秒から始めたい場合は、`<YouTube動画のID>?start=<t>`

## 3. 教材メディアのデータファイルをWebアプリに読み込ませる準備をする。
我々が作成したCSV形式の教材メディアのデータファイルは、そのままの形ではWebアプリが読み込むことができません。
そこで、ユーティリティを用いて、Webアプリが読み込める`tmmdata_tmmf2n.json`へ変換します。
1. `make_tmmdata_json.py`を起動して下さい。これがそのユーティリティです。
2. ここに先ほど作成したCSV形式の教材メディアのデータファイルをドラッグして、Enterキーを押して下さい。
3. `The JSON file already exists. Overwrite?`と出てきたら、既に変換後のファイルが存在していることを示しています。
上書きしてもよいのなら、`y`と書いてEnterキーを押します。
4. `tmmdata_tmmf2n.json`が完成しました。このファイルはWebアプリが読み込むので、名前や内容の変更、移動、削除はしないで下さいね。

## 4. Webアプリを作る。
1. ターミナルを起動し、カレントディレクトリをTMMShowcaseLightに合わせて下さい。
2. この手順を始めて行う方は、以下を実行して下さい。
```
npm install
```
このコマンドを実行することにより、`node_modules`というフォルダができますが、名前や内容の変更、移動、削除はしないで下さい。
3. 以下を実行し、Webアプリを作ります。
```
npm run build
```

## 5. 完成したWebアプリを見る。
1. `webapp_built`というフォルダを開いて下さい。
2. `index.html`を開くと、Webアプリが起動します。
3. このWebアプリを他の人にも使ってもらいたい場合は、以下の2つのファイルを送信します。
  * `index.html`
  * `bundle.js`

# 教材メディアのデータ規格 tmmf2 について
tmmf2は教材メディアのデータの規格です。
人間が作成したCSV形式の教材メディアのデータファイルをWebアプリが読めるように、データの構造を取り決めました。

tmnf2は以下2つの項目を持ちます。
* ドメイン形式 / tmmf2d
  * 人間が読んで編集するための形式です。
  * `TMMData_example_tmvf2d.csv`はこれに準拠しています。
  * `make_tmmdata_json.py'に読み込ませるCSVファイルは必ずこれに準拠している必要があります。
  CSV形式の教材メディアのデータファイルはこれに従いながら作成するのがよいでしょう。
* 正規形式 / tmmf2n
  * Webアプリが読み込むための形式です。
  * `tmmdata_tmmf2n.json`はこれに準拠しています。
  * 正規化されているので、機械が読み込むのに最適な構造をしています。
1つのメディアは`メディアタイプ`と`メディアペイロード`の2つの情報から構成されています。
* メディアタイプ : そのメディアの種類。今のところは1本のYouTube動画しか対応していません。
* メディアペイロード : そのメディアの内容を表す情報です。何の情報をここに書くかは、メディアタイプに依ります。
