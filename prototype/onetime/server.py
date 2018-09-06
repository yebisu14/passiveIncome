# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, jsonify
import hashlib
import sqlite3

app = Flask(__name__)

DB_NAME = "./data.db"

"""
ハッシュのラッパー
あとでアルゴリズムを変更できるようにラップしておく
"""
def hash(x):
    return hashlib.sha256(x).hexdigest()

"""
ユーザからの閲覧リクエストを元に、
コントラクト上に購入履歴があるかどうかを判定、
ある場合はvalid, ない場合はinvalidを返す。
"""
@app.route('/request')
def req():
    encrypted_uuid = request.args.get('euuid')
    print(encrypted_uuid)
    uuid = sk.decrypt(encrypted_uuid)
    print(uuid)
    return uuid


"""
今オープンになっている動画一覧を返す
データベースからサムネイルをひっぱてきて一覧にする
"""
@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    args = []
    for row in cursor.execute("SELECT * FROM thumbnails"):
        args.append(
            {
                'uri': row[1],
                'huuid': str(hash(row[0].encode()))
            }
        )

    return render_template('index.html', args = args)


"""
表示されているサムネイルをクリックされた時に呼ばれる
閲覧リクエストに相当
"""
@app.route('/open')
def request_watching():
    huuid = request.args.get('huuid')

    return "invalid"




if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')