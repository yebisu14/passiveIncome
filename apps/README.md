# apps
サーバサイドアプリケーション

## server.py
動画購入プラットフォームを起動します。





# リクエストの種類の定義
クライアント（動画配信、動画閲覧、動画購入デバイス）とDMMサーバが利用するリクエストの定義を行う。
ただし、購入デバイスと閲覧デバイスは同じものになってもよい（基本的には同じものとする）

#### 配信リクエスト
主に動画配信デバイスが利用する。
下記の処理をまとめて配信リクエストと呼ぶことにする。
1. DMMサーバに対して、自身のウォレットアドレスを登録する。
2. スマコンに自身のウォレットアドレス（と残高）を登録する。
自身のウォレットアドレスを自分の識別子として利用する。
#### 閲覧リクエスト
主に閲覧デバイスが利用する。

#### 購入リクエスト
主に購入デバイスが利用する。


## client.py

## server.py


## URLスキーマ
| エントリーポイント    |       意味                    | 
|  -----             |       -----                  |
|      /             |  現在配信中の動画一覧            |
|  /register?uuid=[UUID] |  配信リクエストを登録する    |




## サーバが保持するデータ

命名規則はとりあえずこの辺にしたがっておく。

https://qiita.com/genzouw/items/35022fa96c120e67c637


### サムネイルテーブル
static/img/thumbnails配下のサムネイルをdevice_wallet_addressと関連づける。

```
CREATE TABLE thumbnails(
    wallet_address TEXT PRIMARY KEY NOT NULL,
    image_uri TEXT
)
```

### ブロードキャストURIテーブル
ウォレットアドレスと配信URLを紐づける。

```
CREATE TABLE broadcast_uris(
    wallet_address TEXT PRIMARY KEY NOT NULL,
    broadcast_uri TEXT
)
```


# 用語の定義など
- 購入UUID、購入番号: 購入情報を特定するためのID。購入者は購入UUIDリストを保持しており、購入UUIDがスマコン上にあることで、正当な購入者であることを証明している。

