# TMMShowcaseLight
教材メディア(Teachin Material Media)の展示Webアプリです。

CSVファイルを用いて展示する教材メディアのデータを与えれば、それらを展示するHTML及びJS形式のWebアプリを生成することができます。

jQueryとBootstrapを使用した軽量なWebアプリです。

# 初心者向け : Webアプリの作り方
## 用意すべきもの
* npm
* python3系
* CSVエディタ : Excelでは正常に開けないCSVファイルを扱うため、その他のソフトを使って下さい。例えば[Cassava](https://www.asukaze.net/soft/cassava/)などがおすすめです。

## ロードマップ
![ロードマップ](https://raw.githubusercontent.com/Mya-Mya/TMMShowcaseLight/main/roadmap/overview.png)

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

# 技術情報 : 教材メディアのデータ規格 tmmf2 について
tmmf2は本リポジトリ内で使用する教材メディアのデータの規格です。
人間が作成したCSVファイルをWebアプリが読めるJSONファイルに変換できるよう、両者のデータの構造を取り決めました。

tmnf2は以下2つの項目を持ちます。
* ドメイン形式 / tmmf2d
  * 人間が読んで編集するためのCSV形式です。
  * `TMMData_example_tmvf2d.csv`はこれに準拠しています。
  * `make_tmmdata_json.py`に読み込ませるCSVファイルは必ずこれに準拠している必要があります。
  * 入れ子等の構造から成り立っているので、人間が読むのに最適な構造をしています。
  CSV形式の教材メディアのデータファイルはこれに従いながら作成するのがよいでしょう。
* 正規形式 / tmmf2n
  * Webアプリが読み込むための形式です。
  * `tmmdata_tmmf2n.json`はこれに準拠しています。
  * 正規化されているので、機械が読み込むのに最適な構造をしています。

## ドメイン形式 / tmmf2d
### CSVファイルの作り方
ファイル形式やエンコーディング、書き方については[## 2. 教材メディアのデータファイルを作る。](https://github.com/Mya-Mya/TMMShowcaseLight/blob/main/README.md#2-%E6%95%99%E6%9D%90%E3%83%A1%E3%83%87%E3%82%A3%E3%82%A2%E3%81%AE%E3%83%87%E3%83%BC%E3%82%BF%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%82%92%E4%BD%9C%E3%82%8B)を参考にして下さい。
この通りに作ればtmmf2dに準拠したCSVファイルを作ることができます。

### 属性
tmmf2dに準拠したCSVファイルは以下のような関係性を持つデータを表しています。

Shelf
* name : str
* lessons : List[Lesson]

Lesson
* name : str
* chapters : List[Chapter]

Chapter
* name : str
* medias : List[Media]

Media
* type : str
* payload : str

## 正規形式 / tmmf2n
### JSONファイルの構造
各要素については[`webapp/tmmf2n.js`](https://github.com/Mya-Mya/TMMShowcaseLight/blob/main/webapp/tmmf2n.js)にて型宣言がなされているので、そちらも参照して下さい。
```
tmmData = 
{
  "shelfIds" : {string[]},
  "lessonIds": {string[]},
  "chapterIds": {string[]},
  "mediaIds": {string[]},
  "shelves" : {
    <shelfId>: {
      "id": <shelfId>,
      "name": <シェルフ名>,
      "lessonIds": {string[]}
    }
  },
  "lessons": {
    <lessonId>: {
      "id": <lessonId>,
      "name": <レッスン名>,
      "chapterIds": {string[]}
    }
  },
  "chapters": {
    <chapterId>: {
      "id": <chapterId>,
      "name": <チャプター名>,
      "mediaIds": {string[]}
    }
  },
  "medias": {
    <mediaId>: {
      "id": <mediaId>,
      "type": <タイプ>,
      "payload": <ペイロード>
    }
  }
}
```

### 属性
tmmf2nに準拠したJSONファイルは以下のような関係性を持つデータを表しています。主キーには`*`が付けられています。

Shelf
* id * : str
* name : str
* lessonIds : List[str]

Lesson
* id * : str
* name : str
* chapterIds : List[str]

Chapter
* id * : str
* name : str
* mediaIds : List[str]

Media
* id * : str
* type : str
* payload : str

## Mediaについて
1つのMediaは`type`と`payload`の2つの情報から構成されています。
* `type` : そのメディアの種類。今のところは1本のYouTube動画しか対応していません。
* `payload` : そのメディアの内容を表す情報です。何の情報をここに書くかは、メディアタイプに依ります。

# 技術情報 : 詳細なロードマップ
![ロードマップ](https://raw.githubusercontent.com/Mya-Mya/TMMShowcaseLight/main/roadmap/detailed.png)
