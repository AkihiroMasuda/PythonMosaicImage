# -*- coding: utf-8 -*-
'''
Created on 2013/08/23

@author: akihiro
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
        num = np.size(labels) #データ数
        indexes = range(num)

    rsses = np.zeros(np.size(indexes), dtype="int")
    for i in indexes:
        # 参照色との残差平方和を求める
        rsses[i] = getColorRSSFromRGB(dict, i, ref_rgb)
        pass
    minind = np.argmin(rsses)
    minrss = rsses[minind]
    return indexes[minind], minrss   
    
    
def putSmallImageOntoLargeImage(largeImage, smallImage, x, y):
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

    # 参照画像を取得
    ref_ind = 2
    ref_image = getRGBTable(dict, ref_ind)
    fname = ("ref%05d" % ref_ind) + ".png"
    pl.imsave(prjpath+"result\\py04\\" + fname, ref_image)

    ticktock.tick()

    range_xy = np.shape(ref_image)
    dest_image = np.zeros([range_xy[0]*32, range_xy[1]*32, 3], dtype='uint8') #uint8で作るのが大事
    for x in range(range_xy[0]):
        print x
        for y in range(range_xy[1]):
            ref_rgb = ref_image[x,y,:]
            # 一番色が近い画像を求める
            [minind, rss] = findNearestColorImage(dict, ref_rgb, range(100))
#             [minind, rss] = findNearestColorImage(dict, ref_rgb, range(10000))
        #     [minind, rss] = findNearestColorImage(dict, ref_rgb)
            # 一番近い画像を取得
            near_rgb = getRGBTable(dict, minind)
            putSmallImageOntoLargeImage(dest_image, near_rgb, x*32, y*32)
            
    ticktock.tock()
     
    # 保存
    pl.imsave(prjpath+"result\\py04\\dest.png",dest_image)

