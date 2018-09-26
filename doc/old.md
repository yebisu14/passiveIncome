

# インストール方法
### スマートコントラクト

`truffle.js`の3箇所を自身のMetaMaskとropsten_networkに合わせてください。

次に下記コマンドでropstenネットワークにデプロイします。実行後、コントラクトアドレスが出力されるので、`CONTRACT_ADRESS`にコピーペーストしてください。

```
$ truffle migrate --network ropsten
```


ABIを取得し、`abi=`にコピーペーストします。

```
$ cat /path/to/Metacoin.json | jq -c .abi
```


### 動画配信デバイス
nginxをrtmpモジュール付きでセットアップしてください。





#### DMMサーバ

`server.py`を開き、ropsten_networkとコントラクトのアドレスを適宜修正してください。

```
INFURA = 
CONTRACT_ADDRESS = 
abi = 
```

下記コマンドによりサーバを立ててください。
```
$python3 server.py
```

# ユースケース





# 問題点など
### 動画配信サーバ
nodejsでh264動画を配信する`h264-live-player`なるものがあるらしいので、これを利用します。
全画面で動画が配信されてラズベリーパイが何も操作をうけつけなくなるが、どうしたらよいのか。

https://qiita.com/okaxaki/items/72226a0b0f5fab0ec9e9



# 調査

- Ropsten
イーサリアムテストネットワーク。

- Infura
Ropstenネットワークに接続するためのイーサリアムクライアント。
gethでも接続できるが、同期が面倒なのでこれを利用。

この辺参考に

https://noumenon-th.net/programming/2018/06/06/truffle_infura/
