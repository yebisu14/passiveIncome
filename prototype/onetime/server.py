# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, jsonify
from Crypto.PublicKey import RSA
from Crypto import Random

"""
公開鍵の作成
"""
random_generator = Random.new().read
sk = RSA.generate(1024, random_generator)
pk = sk.publickey().exportKey(format='PEM', passphrase=None, pkcs=1)

app = Flask(__name__)

"""
ユーザからの購入リクエストをトリガーとし、
公開鍵をユーザに返す
"""
@app.route('/pubkey.pem')
def getPubKey():
    return pk


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
"""



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')