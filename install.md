# ハマったことメモ
- web3.jsのバージョンは1.0.0ではなく、0.20.6なので注意。コールバックの書き方が若干違う。
- pull型だと動画キーの設定ができない。(動的に設定する方法があるのか不明)。
    - $nameでキーを取ってこれるっぽい？




# サーバインストールメモ

## 1.nginxのインストール
- nginx-1.14.0をダウンロード
- nginx-rtmp-moduleをダウンロード
- モジュールを有効にしてコンパイルする

- /usr/local/nginx/ ルート
- /usr/local/nginx/sbin/nginx バイナリの場所
- /usr/local/nginx/conf/nginx.conf 設定ファイルの場所
- /usr/local/nginx/html/rec flv形式で録画されたデータ
- /home/ubuntu/passiveIncome/apps/static/img/thumbnails 切り出したサムネイル画像(index.htmlで表示するため)

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

        # hls動画をflvとして保存する
        record all;
        record_path /usr/local/nginx/html/rec;
        record_suffix -%Y%m%d%H%M%S.flv;

        # サムネイルを登録
        exec_done_record ffmpeg i- $path -ss 1 -t 1 -r 1 image2 test.jpg

        # pullの場合は下記を設定
        # pull rtmp://path/to/hls 
      }
  }
    
}
```

- フォルダの権限変更も忘れずに
- 744じゃないと動かないっぽい

```
$ sudo mkdir /usr/local/nginx/html/rec
$ sudo chown nobody /usr/local/nginx/html/rec
$ sudo chmod 744 /usr/local/nginx/html/rec
```

- ffmpegはこの辺りを参考に
- https://qiita.com/matoken/items/664e7a7e8f31e8a46a60



```
-i 元動画.avi : 元動画
-ss 144 : 抜き出し始点(秒)
-t 148 : 抜き出し終点(秒)
-r 24 : 1秒あたり何枚抜き出すか
-f image2 %06d.jpg : jpeg で[000001.jpg]から連番で書き出し
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

## 3.pythonのセットアップ

- pipを入れる
- pyenvを入れる(pythonは3.5以上でないとweb3が動かない)

```
$ pip3 install web3
$ pip3 install flask
```

```
git clone https://github.com/yyuu/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc
```

- 3.7.0のインストール

```
sudo apt install libffi-dev
pyenv install 3.7.0
pyenv global 3.7.0
pyenv rehash
```


## 4.アプリケーションの実行

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



