# TMMShowcaseLight

教材メディア(Teachin Material Media)の展示 Web アプリです。

CSV ファイルを用いて展示する教材メディアのデータを与えれば、それらを展示する HTML 及び JS 形式の Web アプリを生成することができます。

jQuery と Bootstrap を使用した軽量な Web アプリです。

# 初心者向け : Web アプリの作り方

## 用意すべきもの

- npm
- python3 系
- CSV エディタ : Excel では正常に開けない CSV ファイルを扱うため、その他のソフトを使って下さい。例えば Google Spreadsheet や[Cassava](https://www.asukaze.net/soft/cassava/)などがおすすめです。

## ロードマップ

![ロードマップ](https://raw.githubusercontent.com/Mya-Mya/TMMShowcaseLight/main/roadmap/overview.png)

## 1. 教材メディアの構造を知る。

教材メディアには階層が存在します。それは以下の通りです。

`シェルフ > レッスン > チャプター > メディア`

- メディア : `リチウムの炎色反応の動画`等の、1 つのメディアを表すものです。今対応しているものでは、1 本の YouTube 動画があります。今後需要によってはその他の形式のメディアも対応したいと思っています。
- チャプター : 複数のメディアを束ねたものです。
  例えば授業中、`1.リチウムの炎色反応の動画 2.ナトリウムの炎色反応の動画 3.ホウ素の炎色反応の動画` といったように、生徒さんに見て欲しいメディアが連続して 3 つある場合は、
  `炎色反応`というチャプターの下、これら 3 つのメディアをまとめます。
- レッスン : `化学の授業第3回目`等の、1 回の授業を表す存在です。1 回の授業で、このレッスン下にあるチャプター全てを使います。
- シェルフ : `化学の教科書 上`等の、複数のレッスンを束ねたものです。一連の教材シリーズ、1 冊の教科書、1 冊の本の中での大きな区切りなどを表します。

## 2. 教材メディアのデータファイルを作る。

データはカンマ区切り、**UTF-8 エンコーディングの**CSV ファイルで記述します。
Excel は UTF-8 エンコーディングの CSV ファイルを開けないため、別のソフトで作業する必要があります。
Google Spreadsheet でデータを作り[ファイル]>[ダウンロード]>[カンマ区切りの値]の順番でダウンロードすれば、カンマ区切り、UTF-8 エンコーディングの CSV ファイルを得ることができます。

例えば教材メディアを以下のように配置したいとします。

- シェルフ 1
  - レッスン 1
    - チャプター 1
      - YouTube 動画 youtu.be/vvvvv
      - YouTube 動画 youtu.be/wwwww
    - チャプター 2
      - YouTube 動画 youtu.be/xxxxx
  - レッスン 2
    - チャプター 3
      - YouTube 動画 youtu.be/yyyyyy
- シェルフ 1
  - レッスン 1
    - チャプター 1
      - YouTube 動画 youtu.be/zzzzzz

この際には、本リポジトリ内にある[TMMData_example_tmmf2d.csv](https://github.com/Mya-Mya/TMMShowcaseLight/blob/main/TMMData_example_tmmf2d.csv)のように書きます。

### メディアタイプとメディアペイロードの書き方

1 本の YouTube 動画をメディアとして展示したい場合、以下のように書きます。

- メディアタイプ : `youtube`
- メディアペイロード
  - 通常は、`<YouTube動画のID>`
  - 再生位置を`t`秒から始めたい場合は、`<YouTube動画のID>?start=<t>`

## 3. 教材メディアのデータファイルを Web アプリに読み込ませる準備をする。

我々が作成した CSV 形式の教材メディアのデータファイルは、そのままの形では Web アプリが読み込むことができません。
そこで、ユーティリティを用いて、Web アプリが読み込める`tmmdata_tmmf2n.json`へ変換します。

1. `make_tmmdata_json.py`を起動して下さい。これがそのユーティリティです。
2. ここに先ほど作成した CSV 形式の教材メディアのデータファイルをドラッグして、Enter キーを押して下さい。
3. `The JSON file already exists. Overwrite?`と出てきたら、既に変換後のファイルが存在していることを示しています。
   上書きしてもよいのなら、`y`と書いて Enter キーを押します。
4. `tmmdata_tmmf2n.json`が完成しました。このファイルは Web アプリが読み込むので、名前や内容の変更、移動、削除はしないで下さいね。

## 4. Web アプリを作る。

1. ターミナルを起動し、カレントディレクトリを TMMShowcaseLight に合わせて下さい。
2. この手順を始めて行う方は、以下を実行して下さい。

```
npm install
```

このコマンドを実行することにより、`node_modules`というフォルダができますが、名前や内容の変更、移動、削除はしないで下さい。

3. 以下を実行し、Web アプリを作ります。

```
npm run build
```

## 5. 完成した Web アプリを見る。

1. `webapp_built`というフォルダを開いて下さい。
2. `index.html`を開くと、Web アプリが起動します。
3. この Web アプリを他の人にも使ってもらいたい場合は、以下の 2 つのファイルを送信します。
   - `index.html`
   - `bundle.js`

# 技術情報 : 教材メディアのデータ規格 tmmf2 について

tmmf2 は本リポジトリ内で使用する教材メディアのデータの規格です。
人間が作成した CSV ファイルを Web アプリが読める JSON ファイルに変換できるよう、両者のデータの構造を取り決めました。

tmnf2 は以下 2 つの項目を持ちます。

- ドメイン形式 / tmmf2d
  - 人間が読んで編集するための CSV 形式です。
  - `TMMData_example_tmvf2d.csv`はこれに準拠しています。
  - `make_tmmdata_json.py`に読み込ませる CSV ファイルは必ずこれに準拠している必要があります。
  - 入れ子等の構造から成り立っているので、人間が読むのに最適な構造をしています。
    CSV 形式の教材メディアのデータファイルはこれに従いながら作成するのがよいでしょう。
- 正規形式 / tmmf2n
  - Web アプリが読み込むための形式です。
  - `tmmdata_tmmf2n.json`はこれに準拠しています。
  - 正規化されているので、機械が読み込むのに最適な構造をしています。

## ドメイン形式 / tmmf2d

### CSV ファイルの作り方

ファイル形式やエンコーディング、書き方については[## 2. 教材メディアのデータファイルを作る。](https://github.com/Mya-Mya/TMMShowcaseLight/blob/main/README.md#2-%E6%95%99%E6%9D%90%E3%83%A1%E3%83%87%E3%82%A3%E3%82%A2%E3%81%AE%E3%83%87%E3%83%BC%E3%82%BF%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%82%92%E4%BD%9C%E3%82%8B)を参考にして下さい。
この通りに作れば tmmf2d に準拠した CSV ファイルを作ることができます。

### 属性

tmmf2d に準拠した CSV ファイルは以下のような関係性を持つデータを表しています。

Shelf

- name : str
- lessons : List[Lesson]

Lesson

- name : str
- chapters : List[Chapter]

Chapter

- name : str
- medias : List[Media]

Media

- type : str
- payload : str

## 正規形式 / tmmf2n

### JSON ファイルの構造

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

tmmf2n に準拠した JSON ファイルは以下のような関係性を持つデータを表しています。主キーには`*`が付けられています。

Shelf

- id \* : str
- name : str
- lessonIds : List[str]

Lesson

- id \* : str
- name : str
- chapterIds : List[str]

Chapter

- id \* : str
- name : str
- mediaIds : List[str]

Media

- id \* : str
- type : str
- payload : str

## Media について

1 つの Media は`type`と`payload`の 2 つの情報から構成されています。

- `type` : そのメディアの種類。今のところは 1 本の YouTube 動画しか対応していません。
- `payload` : そのメディアの内容を表す情報です。何の情報をここに書くかは、メディアタイプに依ります。

# 技術情報 : 詳細なロードマップ

![ロードマップ](https://raw.githubusercontent.com/Mya-Mya/TMMShowcaseLight/main/roadmap/detailed.png)
