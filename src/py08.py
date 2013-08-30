# -*- coding: utf-8 -*-
'''
Created on 2013/08/25
@author: akihiro
モザイク画高速化
ParallelPyを使って分散化
mainの入出力を画像データに変更
'''
import numpy 
import Ticktock
import matplotlib.pylab as pl
import math
import os
import pp

import py08_pcalc
import py08_image

def getResultPath():
    '''
          結果保存先のパスを取得
          末尾に'/'は含まない
    '''
    prjpath = "D:\\root\\programing\\Python\\MosaicImage\\" #絶対パスしていでないとインタラクティブモードで失敗する
    dirpath = "data/cifar-10-python.tar/cifar-10-batches-py/"
    resultpath = prjpath+"result"
    resultpath2 = resultpath + "/py08"
    
    if os.path.exists(resultpath) == False:
        os.mkdir(resultpath)
    if os.path.exists(resultpath2 ) == False:
        os.mkdir(resultpath2)
    
    return resultpath2
    
    
def loadSrcImage():
    """
        変換元の画像を取得
    return : RGB配列  MxNx3 [[[R00,G00,B00], [R01,G01,B01], ... ],
                           [[R10,G10,B10], [R11,G11,B11], ... ],
                           ...
                           ]
    """
    prjpath = "D:\\root\\programing\\Python\\MosaicImage\\" #絶対パスしていでないとインタラクティブモードで失敗する
    dirpath = "data/cifar-10-python.tar/cifar-10-batches-py/"
    file = "data_batch_1"
    fullpath = prjpath + dirpath + file
    dict = py08_pcalc.unpickle(fullpath)
    
    # 参照画像を取得
    ref_ind = 2
    ref_image = py08_pcalc.getRGBTable(dict, ref_ind)
    fname = ("ref%05d" % ref_ind) + ".png"
    
    # 参照画像を保存
    pl.imsave( getResultPath() + "/" + fname, ref_image)
     
    return ref_image
     
    
def split_seq(seq, num):
    '''
                入力の配列をnum個に均等に分割
    example)
    in : seq=range(32), num=3
    out: [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], [22, 23, 24, 25, 26, 27, 28, 29, 30, 31]]

    '''
    l = len(seq)
    size = int(math.ceil(float(l)/num))
    return [seq[i:i+size] for i in range(0, len(seq), size)]    
    
def main(srcImg):
    """
    input : 
        srcImg :入力画像配列. サイズ  NxMx3 のRGBのnum.array
    output : 
        return : 出力画像配列.  サイズ  NxMx3 のRGBのnum.array
    """
#     ppservers = ()
#     ppservers = ("192.168.1.242",)
    ppservers = ("192.168.1.243","192.168.1.242", )
#     job_server = pp.Server(1, ppservers=ppservers) #自PCのCPUリソース数を第一引き数で指定。0だと自PCは何もしない
    job_server = pp.Server(0, ppservers=ppservers) #自PCのCPUリソース数を第一引き数で指定。0だと自PCは何もしない
    
    # 時間測定用
    ticktock = Ticktock.Ticktock()

    # 変換元画像を分割
    # 水平方向（X方向）に分割
    num_separate = len(ppservers) #分割数
    size_x = numpy.shape(srcImg)[1]
    columns = split_seq(range(size_x), num_separate)
    ref_img_separated = []
    for i in range(num_separate):
        ref_img_separated.append(srcImg[:,columns[i],:]) 
    
    ticktock.tick() #速度測定開始

    # モザイク画作成
    jobs = []
    for i, img_in in enumerate(ref_img_separated):
        job = job_server.submit(py08_pcalc.makeMosaicImage,
                                 (img_in,),
                                 (py08_pcalc.unpickle, py08_pcalc.calMeans, py08_pcalc.getImageNum, py08_pcalc.getRGB, py08_pcalc.getPIXSIZE,
                                   py08_pcalc.getPIXNUM, py08_pcalc.findNearestColorImageUseMeans, py08_pcalc.findNearestColorImage,
                                    py08_pcalc.getColorRSSFromRGB, py08_pcalc.getRGBTable, py08_pcalc.putSmallImageOntoLargeImage,
                                     py08_pcalc.getCifar10FilePath, py08_pcalc.isExistMenaFile, py08_pcalc.getMeanFilePath, py08_pcalc.saveMeans, py08_pcalc.loadMeans, ),
                                 ("numpy","pickle",))  # 他モジュールに依存関数を入れているが、すべてここで列挙が必要。modulesに書くだけではダメで、むしろそこには書いてはいけない。
#         job = job_server.submit(py08_pcalc.makeMosaicImage,
#                                  (img_in,),
#                                  (,)
#                                  ("numpy","pickle",""py08_pcalc))  # これはだめ。
        jobs.append(job)
        
    # 実行結果を得る
    dest_image = []
    for jo in jobs:
        result = jo()
#         print result
        dest_image.append(result)

    # 変換結果を結合
    dest_image_cat = [] 
    for i, img_out in enumerate(dest_image):
        if i==0:
            dest_image_cat = img_out
        else:
            dest_image_cat = numpy.hstack([dest_image_cat, img_out])
            
    ticktock.tock() #速度測定終了
    
    # レポート表示
    job_server.print_stats()
            
    return dest_image_cat
    

if __name__ == '__main__':
    f = open(getResultPath() + "/input.png", "rb")
    data = f.read()
    srcImg = py08_image.convImgBindata2RGBArray(data)
#     srcImg = loadSrcImage()
    outImg = main(srcImg)
    # 保存
    pl.imsave(getResultPath() + "/dest.png", outImg)

