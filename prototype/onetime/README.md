# prpototype/onetime
ワンタイムURL発行のテストコード

## client.py

## server.py


## URLスキーマ
- query: http://localhost:8080/get?pk=[xxxx]
- response: encrypted uri of movie.

|key |     意味     |
|----|     ----    |
|pk  | ユーザの公開鍵 |

## サーバが保持するデータ

命名規則はとりあえずこの辺にしたがっておく。

https://qiita.com/genzouw/items/35022fa96c120e67c637


### サムネイルテーブル

```
CREATE TABLE thumbnails(
    uuid TEXT PRIMARY KEY NOT NULL,
    image BLOB
)
```

