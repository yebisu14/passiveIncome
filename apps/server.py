# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
import sqlite3
from web3 import Web3, HTTPProvider
import json
import urllib.request
from datetime import datetime
import configparser
import werkzeug

DB_NAME = "./data.db"

config = configparser.ConfigParser()
config.read('./config.ini')

# 定数の設定
contractAddress = config.get('contract', 'contract_address')
abi = config.get('contract', 'abi')
abiJson = json.loads(abi)
infra = config.get('eth', 'infra')

# コントラクト初期化
web3 = Web3(HTTPProvider(infra))
addr = Web3.toChecksumAddress(contractAddress)
contract = web3.eth.contract(abi = abiJson, address = addr)


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
jinja_options = app.jinja_options.copy()                                         
jinja_options.update({                                                      
    'block_start_string': '<%',                                                 
    'block_end_string': '%>',                                                   
    'variable_start_string': '<<',                                              
    'variable_end_string': '>>',                                                
    'comment_start_string': '<#',                                               
    'comment_end_string': '#>'                  
})                                                                               
app.jinja_options = jinja_options    



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
    uuid_purchase = request.args.get('uuid')
    wallet_address = request.args.get('addr')
    walletAddress = Web3.toChecksumAddress(wallet_address)
    # ブロードキャストが有効かチェック
    if not contract.functions.isBroadcastable(walletAddress).call():
        return "Bad device."
    # その動画の購入履歴があるかチェック
    if not contract.functions.verifyPurchase(uuid_purchase, walletAddress).call():
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
    cursor.execute('INSERT INTO thumbnail_uris VALUES(?,?)', [wallet_address, imgUri])
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
    for row in cursor.execute('SELECT * FROM thumbnail_uris'):
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
マイページを表示する
"""
@app.route('/mypage')
def mypage():
    data = {
        'abi': abi,
        'contract_address': contractAddress
    }
    return render_template('mypage.html', data=data)


"""
動画のメタ情報を登録する
"""
@app.route('/register_meta', methods=["POST"])
def register_meta():
    # フォームデータをチェック
    print(request.form)
    uri = request.form['uri']
    name = request.form['name']
    description = request.form['description']
    addr = request.form['addr']
    fileName = ""

    # ファイルが存在するときはファイル名を一時ファイル名にして保存
    if 'thumbnail' in request.files:
        img = request.files['thumbnail']
        fileName = datetime.now().strftime("%Y%m%d_%H%M%S_")
        fileName += werkzeug.utils.secure_filename(img.filename)
        img.save('./static/img/thumbnails/'+fileName)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('REPLACE INTO broadcast_uris VALUES(?, ?)', [addr, uri])
    cursor.execute('REPLACE INTO names VALUES(?, ?)', [addr, name])
    cursor.execute('REPLACE INTO descriptions VALUES(?, ?)', [addr, description])
    if fileName:
        cursor.execute('REPLACE INTO thumbnail_uris VALUES(?, ?)', [addr, fileName])
    conn.commit()
    conn.close()
    return 'OK'


"""
アドレスに紐づいた動画情報(metatag)をJSONリクエストで返す
"""
@app.route('/get_meta', methods=["GET"])
def get_meta():
    addr = request.args['addr']
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    args = {}
    for row in cursor.execute("""
        SELECT name, description, broadcast_uri, thumbnail_uri FROM names, descriptions, broadcast_uris 
        LEFT JOIN thumbnail_uris ON names.wallet_address = thumbnail_uris.wallet_address
        WHERE names.wallet_address = ? and names.wallet_address = descriptions.wallet_address and 
        names.wallet_address = broadcast_uris.wallet_address 
        """, [addr]):
        args['wallet_address'] = addr
        args['name'] = row[0]
        args['description'] = row[1]
        args['uri'] = row[2]
        args['thumbnail'] = row[3]

    conn.close()
    return jsonify(args)
    



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