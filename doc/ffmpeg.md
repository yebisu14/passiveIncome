# ffmpeg調査(途中)

- ffmpegをmp4にする
- https://qiita.com/uupaa/items/c76c76cb149470bf89f2

```
$ ffmpeg -i https://example.com/.../playlist.m3u8 -movflags faststart -c copy -bsf:a aac_adtstoasc rec.mp4
```

- 下記movflagsは動画のメタデータを先頭にもってくるらしい
- 多分必須

```
-movflags faststart
```

- 画像にするならこいつ
- http://www.slab.ces.kyutech.ac.jp/~saitoh/ja/ffmpeg.html

```
動画像（input.mp4）から初期フレーム画像（ファイル名は001.jpg）のみを保存する。
ffmpeg -i input.mp4 -ss 1 -vframes 1 -f image2 001.jpg
-ss 1：1秒目から処理する
-vframes 1：1フレームを対象にする
-f images：画像として出力する
```

- ということはこの辺でいける？

```
ffmpeg -i $path -moveflags faststart -ss 1 -vframes 1 -f image2 /home/ubuntu/passiveIncome/apps/static/thumbnails/$filename.jpg
```

- ていうかflaskがアクセスするタイミングで撮ってくればいいんじゃない？

```
ffmpeg -i $path -moveflags faststart -ss 1 -vframes 1 -f image2 /home/ubuntu/passiveIncome/apps/static/thumbnails/$filename.jpg
```

- macから叩いてみる
- おおできたっぽい


```
$ffmpeg -i rtmp://13.231.137.35/live/test -movflags faststart -ss 1 -vframes 1 -f image2 ~/test.jpg
```

- AWSでも叩いてみる
```
$ffmpeg -i rtmp://localhost/live/test -movflags faststart -ss 1 -vframes 1 -f image2 ~/test.jpg
```