# -*- coding:utf-8 -*-
'''
Created on 2013/08/29
p02_s_bottle と通信するクライアント側のサンプル
@author: akihiro
'''
import httplib
import py08_posthelper as helper

def post_send_file():
#     conn = httplib.HTTPConnection('localhost:8080')
#     conn.re
    dir_path = "../result/py08/"
    url = "http://localhost:8080/posttest"  
    postdata = {"fileUpload": open(dir_path + "input.png", "r+b")}  
    resp = helper.open_url(url, postdata) 
    return resp.read()
#     return resp

def get_dat():
    conn = httplib.HTTPConnection('localhost:8080')
    # conn.request( "GET", "/static/icon" )
    conn.request( "GET", "/static2/icon.png" )
    # conn.request( "GET", "/helloa" )
    res = conn.getresponse()
    
    print(res.status, res.reason)
    print(res.length)
    
    dat = res.read()
    print('len : ' + str(len(dat)))
    # print( dat.decode( "UTF-8" ) )
    
    conn.close()
    
    #受信ファイルデータをそのまんまコピーする
    with open("p02_c_readdata.png", 'wb') as open_file:
        open_file.write(dat)


if __name__ == '__main__':
    print post_send_file()
#     get_dat()
    pass