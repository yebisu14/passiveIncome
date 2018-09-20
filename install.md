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
- pullで設定

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



## 3.アプリケーションの実行

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

- nginxを入れる(1.14.0を使用)

```
wget http://nginx.org/download/nginx-1.8.0.tar.gz
sudo wget http://nginx.org/download/nginx-1.8.0.tar.gz
tar -zxvf nginx-1.8.0.tar.gz
wget https://github.com/arut/nginx-rtmp-module/archive/master.zip
unzip master.zip
wget https://www.openssl.org/source/openssl-1.1.0f.tar.gz
tar xzvf openssl-1.1.0f.tar.gz

cd nginx-1.8.0
./configure --with-http_ssl_module --add-module=../nginx-rtmp-module-master
make
make install
```

- nginxの設定

```
rtmp {
   server {
      listen 1935;
      chunk_size 4096;

      application live {
         live on;
         record off;
      }
   }
}
```

- 自身のrtmpサーバにgstremaerで配信

```
$ gst-launch-1.0 rpicamsrc preview=0 bitrate=1000000 ! video/x-h264, width=1920, height=1080, framerate='30/1' ! h264parse ! flvmux ! rtmpsink location='rtmp://0.0.0.0/live/test'
```



