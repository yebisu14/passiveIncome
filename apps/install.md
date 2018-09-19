# サーバインストールメモ

## 1.nginxのインストール
- nginx-1.14.0をダウンロード
- nginx-rtmp-moduleをダウンロード
- モジュールを有効にしてコンパイルする

- /etc/local/nginx/ ルート
- /etc/local/sbin/nginx バイナリの場所
- /etc/local/conf/nginx.conf 設定ファイルの場所

## 2.nginxの設定
- nginx.confに、rtmp配信サーバの設定を追記する

```
rtmp {
  server {
      listen 1935;
      chunk_size 4096;

      application live {
        live on;
        hls on;
        
        hls_path /usr/local/nginx/html/hls;
        hls_fragment 1s;
        hls_type live;   
      }
  }
    
}
```

- nginx.confに、uwsgi経由でflaskを動かす設定をする
- hlsフォルダを見えるようにする
- http.server.locationの部分を書き換える

```
http{
    server {
        (省略)
        location / {
            # flask
            include uwsgi_params;
            uwsgi_pass unix:///tmp/uwsgi.sock;
        }

        location /hls {
            alias /usr/local/nginx/html/hls;
        }
```



## 3.アプリケーションのインストール

```
$ git clone 
$ cd passiveIncome/app
$ uwsgi --ini uwsgi.ini
```




# ラズパイインストールめも

- gstremaerを入れる

```
$ sudo apt-get install -y gstreamer1.0 gstreamer1.0-tools gstramer1.0-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
```

- ビルドツール入れる

```
$ sudo apt-get install autoconf automake libtool
```

- rpicamsecを入れる

```
$ git clone https://github.com/thaytan/gst-rpicamsrc.git
$ cd gst-rpicamsrc
$ ./autogen.sh --prefix=/usr --libdir=/usr/lib/arm-linux-gnueabihf/
$ make
$ sudo make install
```

- コマンド実行
