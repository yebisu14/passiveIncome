# -*- coding: utf-8 -*-

import urllib.request
import json
from hashlib

"""
1. 購入リクエストの送信
購入リクエストは、コントラクトに書き込むフェーズからなる。
"""
def sendPurchaseRequest():
    # hash化

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