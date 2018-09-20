# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
import sqlite3
from pathlib import Path

"""
定数
"""
DB_NAME = "./data.db"

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
    # 動画リストを取得
    path = Path("/usr/local/nginx/html/hls")
    playlists = []
    for playlist in list(path.glob('*.m3u8')):
        playlists.append({
            'key': playlist.stem
        })

    return render_template('index.html', playlists=playlists)


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
    key = request.args.get("key", type=str)
    return render_template('watch.html', key=key)





if __name__ == '__main__':
    app.run()
