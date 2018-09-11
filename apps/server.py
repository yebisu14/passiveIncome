# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
import sqlite3
from web3 import Web3, HTTPProvider
import json
import urllib.request
from datetime import datetime

DB_NAME = "./data.db"
INFURA = "https://ropsten.infura.io/v3/35d7622ec4464668b44f8313abfc09a9"
CONTRACT_ADDRESS = "0xd329d886f1131c43bb62966755761ecaa16e9318"


def initContract():
    # コントラクト初期化
    web3 = Web3(HTTPProvider(INFURA))
    #web3.eth.defaultAccount = web3.eth.accounts[0]
    contractAddress = Web3.toChecksumAddress(CONTRACT_ADDRESS)
    abi = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"constant":false,"inputs":[{"name":"purchaseUuid","type":"string"},{"name":"deviceWalletAddress","type":"address"}],"name":"addPurchase","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"deviceWalletAddress","type":"address"}],"name":"addDevice","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"addr","type":"address"}],"name":"isBroadcastable","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"purchaseUuid","type":"string"},{"name":"walletAddress","type":"address"}],"name":"verifyPurchase","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"}]'

    abiJson = json.loads(abi)
    contract = web3.eth.contract(abi = abiJson, address = contractAddress)
    print("Contract was regulated.")
    return contract


def saveQrCode(walleAddress):
    url = 'https://chart.googleapis.com/chart'
    params = {
        'chs': '300x300',
        'cht': 'qr',
        'chl': walleAddress,
        'choe': 'UTF-8'
    }
    req = '{}?{}'.format(url, urllib.parse.urlencode(params))
    urllib.request.urlretrieve(req, 'static/img/qrcodes/{}.png'.format(walleAddress))


app = Flask(__name__)




"""
表示されているサムネイルをクリックされた時に呼ばれる
閲覧リクエストに相当

サーバはスマートコントラクトに対して、
1. 購入済みチェックを行う
2. 配信チェックを行う
どちらかが不可能なら、invalidを返す
"""
@app.route('/watch')
def request_watching():
    contract = initContract()
    uuid_purchase = request.args.get('uuid')
    wallet_address = request.args.get('addr')
    # ブロードキャストが有効かチェック
    if not contract.functions.isBroadcastable(wallet_address).call():
        return "Bad device."
    # その動画の購入履歴があるかチェック
    if not contract.functions.verifyPurchase(uuid_purchase, wallet_address).call():
        return "No histories of purchase."
    # DMMのサーバ上にあるDBを見てURIを参照
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    uri = ""
    for row in cursor.execute('SELECT * FROM broadcast_uris WHERE wallet_address=?', [wallet_address]):
        uri = row[1]
    return uri

"""
配信リクエストを登録する
"""
@app.route('/broadcast')
def request_broadcast():
    imgUri = request.args.get('img_uri')
    broadcastUri = request.args.get('broadcast_uri')
    wallet_address = request.args.get('addr')
    # アドレスからQRコードを作成
    saveQrCode(wallet_address)
    # DMMのサーバ上にあるDBにブロードキャストURIを登録
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO broadcast_uris VALUES(?,?)', [wallet_address, broadcastUri])
    # DMMのサーバ上にあるDBにサムネイルを登録
    cursor.execute('INSERT INTO thumbnails VALUES(?,?)', [wallet_address, imgUri])
    conn.commit()
    conn.close()
    return "OK."

"""
サムネイルのアップロード
成功した場合はファイル名が帰る
失敗した場合はステータスが帰る
"""
@app.route('/upload', methods=['POST'])
def upload_image():
    # ファイルがあるかどうかのチェック
    if 'img' not in request.files:
        return make_response(jsonify({
            'result':'uploadFile is required.',
            'status': 'NG'
        }))
    
    # サムネイルサイズが正しいかどうかのチェック
    
    # ファイルが存在するときはファイル名を一時ファイル名にして保存
    file = request.files['img']
    fileName = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
    file.save('./static/img/thumbnails/'+fileName)

    # ファイル名をレスポンスとして返す
    return make_response(jsonify({
        'status': 'OK',
        'filename': fileName
    }))




"""
今オープンになっている動画一覧を返す
データベースからサムネイルをひっぱてきて一覧にする
"""
@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    args = []
    for row in cursor.execute('SELECT * FROM thumbnails'):
        args.append(
            {
                'wallet_address': row[0],
                'uri_thumbnail': row[1],
                'uri_qrcode': '{}.png'.format(row[0])
            }
        )
    conn.close()
    return render_template('index.html', args = args)


"""
データ消す
"""
@app.route('/del')
def delete():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM thumbnails')
    cursor.execute('DELETE FROM broadcast_uris')
    conn.commit()
    conn.close()
    return 'OK'


"""
購入一覧
"""
@app.route('/histories')
def histories():
    return render_template('histories.html')




if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')