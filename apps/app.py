# -*- coding: utf-8 -*-

"""
最小限のFlask鯖
"""

from flask import Flask, render_template

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


@app.route('/')
def hello():
    return 'Hello, World!'


"""
動画視聴URLを返す
HLSストリーミングを表示する
"""
@app.route('/watch')
def watch():
    return render_template('watch.html', movie_uri="test.mp4")





if __name__ == '__main__':
    app.run()
