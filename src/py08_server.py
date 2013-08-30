# -*- coding:utf-8 -*-
'''
Created on 2013/08/30
モザイク画作成サーバ
@author: akihiro
'''
import os
from bottle import route, run, get, post, request, static_file, template
import time
import py08

# postでバイナリデータを送ってみる例
@post('/posttest') # or @route('/login', method='POST')
def do_posttest():

    upload     = request.files.get('fileUpload') #ファイルのデータ取得
    name, ext = os.path.splitext(upload.filename) #ファイル名を分割
#     save_path = "./"
    save_path = "../result/py08/server/"

    #受信ファイルデータをそのまんまコピーする
    with open(save_path + name + ext, 'wb') as open_file:
        rdat = upload.file.read() #あまり大きなデータの時はまずいらしい
        open_file.write(rdat)
        return "OK : readdata=%d [Byte]" % len(rdat)
         
    return "NG"

# get でバイナリデートを受信してみる例
# http://localhost:8080/hogehoge
# とすると hogehoge が取得できる
# 拡張子を最後に入れるとどうもうまく行かない
@get('/static/<filename>')
def send_static(filename='icon'):
    print 'send_static called' 
    print filename
    return static_file(filename, root='./', download=filename)

# コレ必要
run(host='localhost', port=8080, debug=True)

