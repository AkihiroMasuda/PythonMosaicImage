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
import py08_image
import matplotlib.pylab as pl

def getDirPath():
    return "../result/py08/server/"

# postでバイナリデータを送ってみる例
@post('/posttest') # or @route('/login', method='POST')
def do_posttest():

    upload     = request.files.get('fileUpload') #ファイルのデータ取得
    name, ext = os.path.splitext(upload.filename) #ファイル名を分割
#     save_path = "./"
    save_path = getDirPath() 

    #受信ファイルデータをそのまんまコピーする
    with open(save_path + name + ext, 'wb') as open_file:
        rdat = upload.file.read() #あまり大きなデータの時はまずいらしい
        open_file.write(rdat)
        
        srcImg = py08_image.convImgBindata2RGBArray(rdat)
        outImg = py08.main(srcImg)
        
        print "hogehoge"
        
        #一旦pngファイルとして保存してから返却
        ret_filename = "outImg2.png"
        save_full_path = save_path + ret_filename
        pl.imsave(save_full_path, outImg)
        #保存したのを直ぐ開く
#         f = open(save_full_path, "rb")
#         data = f.read()
    
        print "hogehoge2"

        ret = static_file(ret_filename, root=getDirPath(), download=ret_filename)
        return ret
        
#         return "OK : readdata=%d [Byte]" % len(rdat)
#         return 
         
    return "NG"

# get でバイナリデートを受信してみる例
# http://localhost:8080/hogehoge
# とすると hogehoge が取得できる
# 拡張子を最後に入れるとどうもうまく行かない
@get('/static/<filename>')
def send_static(filename='icon'):
    print 'send_static called' 
    print filename
    return static_file(filename, root=getDirPath(), download=filename)

# コレ必要
run(host='localhost', port=8080, debug=True)
