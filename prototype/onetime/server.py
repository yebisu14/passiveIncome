# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from web3 import Web3, HTTPProvider
import json

DB_NAME = "./data.db"

def initContract():
    # コントラクト初期化
    web3 = Web3(HTTPProvider('http://localhost:9545'))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    contractAddress = Web3.toChecksumAddress("0x057d2360abbe75f9fdf142f2cfe68cfc9a74ec12")
    abi = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"constant":false,"inputs":[{"name":"purchaseUuid","type":"string"},{"name":"deviceWalletAddress","type":"address"}],"name":"addPurchase","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"deviceWalletAddress","type":"address"}],"name":"addDevice","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"addr","type":"address"}],"name":"isBroadcastable","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"purchaseUuid","type":"string"},{"name":"walletAddress","type":"address"}],"name":"verifyPurchase","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"}]'

    abiJson = json.loads(abi)
    contract = web3.eth.contract(abi = abiJson, address = contractAddress)
    print("Contract was regulated.")
    return contract






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
    uuid_purchase = request.args.get('pid')
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
    uri = request.args.get('uri')
    wallet_address = request.args.get('addr')
    # DMMのサーバ上にあるDBにURIを登録
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO broadcast_uris VALUES(?,?)', [wallet_address, uri])
    conn.commit()
    conn.close()
    return "OK."




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
                'uri': row[1],
                'huuid': str(hash(row[0].encode())),
            }
        )
    conn.close()
    return render_template('index.html', args = args)






if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')