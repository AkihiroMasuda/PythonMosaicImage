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

def getDirPath():
    return "../result/py08/server/"

# postでバイナリデータを送ってみる例
@post('/posttest') # or @route('/login', method='POST')
def do_posttest():
    print 'connection accepted'

    workers     = tuple(request.params.get('workers', 'NONE').split(',')) #分散処理対象のPCのIP
    numsOfSampleImages  = int(request.params.get('numOfSampleImages', '100'))
    src_long_size       = int(request.params.get('srcLongSize', '32')) #元画像を縮小したあとの長辺長さ
    upload      = request.files.get('fileUpload') #ファイルのデータ取得
    name, ext   = os.path.splitext(upload.filename) #ファイル名を分割
    
#     save_path = "./"
    save_path = getDirPath() 

    #受信ファイルデータをそのまんまコピーする
    with open(save_path + name + ext, 'wb') as open_file:
        rdat = upload.file.read() #あまり大きなデータの時はまずいらしい
        open_file.write(rdat)
        
    #入力画像を整える
    img_org = py08_image.createImageFromBindata(rdat)
    size_org = img_org.size
#     src_long_size = 32 #長辺が合わせるべき長さ
    if size_org[0] < size_org[1]:
        size_resized = (int(float(size_org[0])/size_org[1]*src_long_size), src_long_size)
    else:
        size_resized = (src_long_size, int(float(size_org[1])/size_org[0]*src_long_size))
    img_resized = py08_image.resizeImgBinData(rdat, size_resized[0], size_resized[1])
    srcImg = py08_image.convImg2Array(img_resized, img_resized.mode)

    # 分散処理実施
    outImg = py08.main(srcImg, workers, numsOfSampleImages)
    
    #一旦pngファイルとして保存してから返却
    ret_filename = "outImg2.png"
    save_full_path = save_path + ret_filename
#         pl.imsave(save_full_path, outImg)
    py08_image.convRGBAArray2Imgfile(outImg, save_full_path)

    ret = static_file(ret_filename, root=getDirPath(), download=ret_filename)
    ret.add_header('Access-Control-Allow-Origin', '*')
    return ret
         
#     return "NG"

# get でバイナリデートを受信してみる例
# http://localhost:8080/hogehoge
# とすると hogehoge が取得できる
# 拡張子を最後に入れるとどうもうまく行かない
@get('/static/<filename>')
def send_static(filename='icon'):
    print 'send_static called' 
    print filename
    ret = static_file(filename, root=getDirPath(), download=filename)
    ret.add_header('Access-Control-Allow-Origin', '*')
    return ret

# コレ必要
run(host='localhost', port=8080, debug=True)
# run(host='192.168.1.253', port=8080, debug=True)
# run(host='192.168.1.243', port=8080, debug=True)

