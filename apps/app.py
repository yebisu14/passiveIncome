# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
import sqlite3
from pathlib import Path
from web3 import Web3, HTTPProvider
import configparser
import json

"""
定数
"""
DB_NAME = "./data.db"

"""
コントラクト設定
"""
config = configparser.ConfigParser()
config.read('./config.ini')
contractAddress = config.get('contract', 'contract_address')
abi = config.get('contract', 'abi')
abiJson = json.loads(abi)
infra = config.get('eth', 'infra')
web3 = Web3(HTTPProvider(infra))
addr = Web3.toChecksumAddress(contractAddress)
contract = web3.eth.contract(abi = abiJson, address = addr)

app = Flask(__name__)

"""
Vue.js対応のおまじない
"""
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
今オープンになっている動画一覧を返す
データベースからサムネイルをひっぱてきて一覧にする
"""
@app.route('/')
def index():
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    args = []
    for row in cursor.execute('SELECT * FROM thumbnail_uris'):
        args.append(
            {
                'wallet_address': row[0],
                'uri_thumbnail': row[1],
                #'uri_qrcode': '{}.png'.format(row[0])
            }
        )
    conn.close()
    """
    # 現在放映中の動画リストを取得
    # 今は使っていない
    path = Path("/usr/local/nginx/html/hls")
    playlists = []
    for playlist in list(path.glob('*.m3u8')):
        playlists.append({
            'key': playlist.stem
        })

    return render_template('index.html', playlists=playlists, abi=abi, contractAddress=contractAddress)


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
動画視聴URLを返す
HLSストリーミングを表示する
"""
@app.route('/watch')
def watch():
    # 購入チェック
    #    if not contract.functions.verifyPurchase(uuid_purchase, walletAddress).call():
        
    key = request.args.get("key", type=str)
    return render_template('watch.html', key=key)

    # 購入されていない場合は購入画面へリダイレクト
    
"""
購入一覧
"""
@app.route('/histories')
def histories():
    return render_template('histories.html')


######################################################################
#
#   ここからAPI
#
#
########################################################################

"""
動画のサムネイルをbase64で取得する
GET /api/thumbnails?key=[movie_key]
ストリーミングのキーを指定します

レスポンスサンプル(json)
{
    img64: [base64_encoded_str]
}


ffmpeg-pythonはうまくいかないのでexecでごり押しした
"""

import subprocess
import base64
import ffmpeg

@app.route('/api/get_thumbnail')
def get_thumbnail():
    key = request.args.get("key", type=str)
    url = 'rtmp://localhost/live/' + key

    path = "/home/ubuntu/tmp/" + key + ".jpg"
    cmd = 'ffmpeg -i %s -movflags faststart -ss 1 -vframes 1 -f image2 %s' % (url, path, )

    subprocess.run(cmd.split(' '), stdout=subprocess.PIPE)
    #img64 =  +  base64.b64encode(open(path, 'rt').read())
    with open(path, 'rb') as b:
        img64 = "data:image/jpeg;base64," + base64.b64encode(b.read()).decode("utf-8")
    
    return img64



if __name__ == '__main__':
    app.run()
