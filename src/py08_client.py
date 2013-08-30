# -*- coding:utf-8 -*-
'''
Created on 2013/08/29
p02_s_bottle と通信するクライアント側のサンプル
@author: akihiro
'''
import httplib
import py08_posthelper as posthelper
import py08_image

def getDirPath():
    return "../result/py08/client/"

def post_send_file():
    dir_path = getDirPath() 
    url = "http://localhost:8080/posttest"  
    postdata = {"fileUpload": open(dir_path + "input.png", "r+b")}  
    resp = posthelper.open_url(url, postdata) 
    return resp.read()

def get_dat():
    conn = httplib.HTTPConnection('localhost:8080')
    # conn.request( "GET", "/static/icon" )
    conn.request( "GET", "/static/icon" )
    # conn.request( "GET", "/helloa" )
    res = conn.getresponse()
    
    print(res.status, res.reason)
    print(res.length)
    
    dat = res.read()
    print('len : ' + str(len(dat)))
    
    conn.close()
    
    #受信ファイルデータをそのまんまコピーする
    with open("p02_c_readdata.png", 'wb') as open_file:
        open_file.write(dat)


if __name__ == '__main__':
    dat = post_send_file()
    print "len : " + str(len(dat))
    with open(getDirPath() + "py08_client_get.png", 'wb') as open_file:
        open_file.write(dat)
    pass