# -*- coding: utf-8 -*-

import urllib.request
import json
from Crypto.PublicKey import RSA


"""
1. 購入リクエストの送信
購入リクエストは、DMMの公開鍵を取得してくるフェーズと、コントラクトに書き込むフェーズからなる。
"""
def sendPurchaseRequest():
    # DMMの公開鍵を取得してくる
    req = 'http://0.0.0.0:5000/pubkey.pem'
    response = urllib.request.urlopen(req)
    key = response.read()

    # 取得した公開鍵を利用して暗号化したUUIDをコントラクト上に載せる
    pub_key = RSA.importKey(key, passphrase=None) 
    euuid = pub_key.encrypt(12345678, 32)[0]
    print(euuid)
    
    # コントラクトに書き込む

    return euuid

"""
2. 閲覧リクエストの送信
自分が見たい暗号化済みのUUIDを送ると、動画を見るためのURLを取得することができる。
"""
def sendReadingRequest(euuid):
    url = 'http://0.0.0.0:5000/request'
    params = {
        'euuid': euuid,
    }
    req = urllib.request.Request('{}?{}'.format(url, urllib.parse.urlencode(params)))
    response = urllib.request.urlopen(req)
    uuid = response.read()
    print(uuid)



euuid = sendPurchaseRequest()
sendReadingRequest(euuid)