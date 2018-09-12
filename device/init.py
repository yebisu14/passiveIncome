# -*- coding: utf-8 -*-

import requests
import json
from web3 import Web3, HTTPProvider
import urllib
import configparser


"""
サムネイルのアップロード
"""
def upload():
    url = 'http://0.0.0.0:5000/upload'
    files = {
        'img': open("lena.png", "rb")
    }
    #url = '{}?{}'.format(url, urllib.parse.urlencode(params)))
    response = requests.post(url, files=files)
    response = json.loads(response.text)
    if(response['status'] == "OK"):
        return response['filename']
    
    return None


"""
配信リクエストの送信
デバイスの登録を行いたい
@param contract
@param walletAddress 自分のウォレットのID
@param uri 自分が配信しているURI
"""
def sendBroadcastRequest(walletAddress, imgUri, broadcastUri):

    # DMMに登録する、URLもいるのかな？
    url = 'http://0.0.0.0:5000/broadcast'
    params = {
        'addr': walletAddress,
        'img_uri': imgUri,
        'broadcast_uri': broadcastUri
    }
    req = urllib.request.Request('{}?{}'.format(url, urllib.parse.urlencode(params)))
    response = urllib.request.urlopen(req)
    res = response.read()
    print(res)



# 設定
config = configparser.ConfigParser()
config.read('config.ini')

walletAddress = config.get('general', 'account_address')
broadcastUri = config.get('general', 'broadcast_uri')

# サムネイルのアップロード
imgUri = upload()

# ブロードキャスト登録
sendBroadcastRequest(walletAddress, imgUri, broadcastUri)


