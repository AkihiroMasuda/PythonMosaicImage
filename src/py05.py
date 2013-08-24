# -*- coding: utf-8 -*-
'''
Created on 2013/08/23
@author: akihiro
モザイク画高速化

'''
import numpy as np
import numpy.random as rnd
import matplotlib.pylab as pl
from numpy.random import * 
import Ticktock
import time
import os
import sys
import Image

PIXNUM = 32
PIXSIZE = PIXNUM*PIXNUM 



def unpickle(file):
    '''
    CIFAR-10画像データ（Python用）を読み込む
    return : dict  ...  dict['data'] : 32x32ピクセルデータ。赤が32x32続いたのち、緑、青と続くフォーマット。
                        dict['labels'] : 画像のラベル  0～9の値をとる
    '''
    import cPickle
    fo = open(file, 'rb')
    dict = cPickle.load(fo)
    fo.close()
    return dict

def getRGB(dict, index):
    data = dict['data']
    
    curimg = data[index]
    r = curimg[0:PIXSIZE]
    g = curimg[PIXSIZE:PIXSIZE*2]
    b = curimg[PIXSIZE*2:]
    
    return r,g,b

def getImageNum(dict):
    '''
           画像 データ数を得る    
    '''
    labels = dict['labels']
    return np.size(labels)

def calMeans(dict):
    '''
    CIFAR-10画像データそれぞれの平均色を算出
    '''
    data = dict['data']
    num = getImageNum(dict)
    means = np.zeros([num, 3], 'uint8')
    for i in range(num):
        [r, g, b] = getRGB(dict, i)
        m_r = int(np.mean(r))
        m_g = int(np.mean(g))
        m_b = int(np.mean(b))
        means[i,:] = [m_r, m_g, m_b]
        
    return means

def getRGBTable(dict, index):
    '''
        ロードしたdictから指定インデックスのRGB配列(32x32x3)を得る。
    [[p0_r, p0_g, p0_b], [p1_r, p1_g, p1_b], ..., [p31_r, p31_g, p31_b]],
    [[p32_r, p32_g, p32_b],                  ...,                      ],
    ]
    '''
    [r, g, b] = getRGB(dict, index)
    rgb = np.vstack([r,g,b])
    rgb = np.reshape(rgb.T, [PIXNUM, PIXNUM, 3])
    return rgb

def getColorRSSFromRGB(dict, index, ref_rgb):
    '''
    indexで指定した画像の ref_rgb との残差平方和RSSを求める
    '''
    [r, g, b] = getRGB(dict, index)
    m_r = ref_rgb[0]
    m_g = ref_rgb[1]
    m_b = ref_rgb[2]
    diff_r = np.mat(r,dtype='int')-m_r
    diff_g = np.mat(g,dtype='int')-m_g
    diff_b = np.mat(b,dtype='int')-m_b
    diff_rgb = np.vstack([diff_r, diff_g, diff_b])
    rss = np.sum(np.power(diff_rgb,2))
    return rss

def findNearestColorImage(dict, ref_rgb, indexes=None):
    '''
    ref_rgb との残差平方和RSSが最小の画像を探す
    '''
    if indexes==None:
        labels = dict['labels'] 
        num_all = np.size(labels) #データ数
        indexes = range(num_all)

    num = np.size(indexes)

    rsses = np.zeros(np.size(indexes), dtype="int")
#     for i in indexes:
    for i in range(num):
        # 参照色との残差平方和を求める
        rsses[i] = getColorRSSFromRGB(dict, indexes[i], ref_rgb)
        pass
    minind = np.argmin(rsses)
    minrss = rsses[minind]
    return indexes[minind], minrss   

def findNearestColorImageUseMeans(dict, ref_rgb, means, num_threashold, indexes=None):
    '''
    ref_rgb との残差平方和RSSが最小の画像を探す
        画像の平均色を使い高速化
        平均色が近いものだけをRSS計算の対象とする
    '''
    
    if indexes==None:
        labels = dict['labels'] 
        num = np.size(labels) #データ数
        indexes = range(num)
    else :
        num = np.size(indexes)

    #平均色と指定色のRSS算出
    means_p = means[indexes, :]
    means_p_deff = means_p - np.ones([num, 1])*np.mat(ref_rgb)
    means_p_rss = np.sum(np.power(means_p_deff, 2),1) 
    
    #平均色のRSSをソート
    means_p_sort_indexes = np.argsort(means_p_rss.A1) #昇順
    means_p_sort = np.sort(means_p_rss.A1)

    #画素毎のRSSによる評価対象とする数
    if num < num_threashold:
        num_threashold = num

    #平均色RSSの小さい上位nu_threasholdまでを抽出
    indexes_tar = np.array(indexes)[means_p_sort_indexes[:num_threashold]]

    #画素毎のRSSが小さい物を選ぶ
    return findNearestColorImage(dict, ref_rgb, indexes_tar)

    
def putSmallImageOntoLargeImage(largeImage, smallImage, x, y):
    '''
    smallImageをlargeImage上の座標x,yに配置する
    x,yにはsmallImageの左上が配置される
    '''
    xsize = np.shape(smallImage)[0]
    ysize = np.shape(smallImage)[1]
    largeImage[x:x+xsize, y:y+ysize, :] = smallImage
    
if __name__ == '__main__':
    # CIFAR-10画像の読み込み
    print sys.argv[0]
#     [pardir, cur] =  os.path.split(os.path.dirname(__file__))
#     [pardir, cur] =  os.path.split(os.path.dirname(sys.argv[0]))
#     prjpath = pardir + "\\"
    prjpath = "D:\\root\\programing\\Python\\MosaicImage\\" #絶対パスしていでないとインタラクティブモードで失敗する
    dirpath = "data/cifar-10-python.tar/cifar-10-batches-py/"
    file = "data_batch_1"
    fullpath = prjpath + dirpath + file
    dict = unpickle(fullpath)
    
    data = dict['data']
    labels = dict['labels'] 
    num = np.size(labels) #データ数

    ticktock = Ticktock.Ticktock()

    # 平均値一覧を取得
    means = calMeans(dict)

    # 参照画像を取得
    ref_ind = 2
    ref_image = getRGBTable(dict, ref_ind)
    fname = ("ref%05d" % ref_ind) + ".png"
    resultpath = prjpath+"result"
    resultpath2 = resultpath + "/py04"
    if os.path.exists(resultpath) == False:
        os.mkdir(resultpath)
    if os.path.exists(resultpath2 ) == False:
        os.mkdir(resultpath2)
    pl.imsave(resultpath2 + "/" + fname, ref_image)

    ticktock.tick()

    range_xy = np.shape(ref_image)
    dest_image = np.zeros([range_xy[0]*32, range_xy[1]*32, 3], dtype='uint8') #uint8で作るのが大事
    for x in range(range_xy[0]):
        print x
        for y in range(range_xy[1]):
            ref_rgb = ref_image[x,y,:]
            # 一番色が近い画像を求める
#             [minind2, rss2] = findNearestColorImage(dict, ref_rgb, range(100))
#             ind3 = range(100)
            num_threashold=50
            [minind, rss] = findNearestColorImageUseMeans(dict, ref_rgb, means, num_threashold, range(10000))
            # 一番近い画像を取得
            near_rgb = getRGBTable(dict, minind)
            putSmallImageOntoLargeImage(dest_image, near_rgb, x*32, y*32)
            
    ticktock.tock()
     
    # 保存
    pl.imsave(resultpath2 + "/dest.png", dest_image)

