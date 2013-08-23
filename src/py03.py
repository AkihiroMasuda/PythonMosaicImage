# -*- coding: utf-8 -*-
'''
Created on 2013/08/23
@author: akihiro
特定色に近い画像を求める
'''
import numpy as np
import numpy.random as rnd
import matplotlib.pylab as pl
from numpy.random import * 
import Ticktock
import time
import os, sys

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
    

if __name__ == '__main__':
    # CIFAR-10画像の読み込み
    [pardir, cur] =  os.path.split(os.path.dirname(__file__))
    prjpath = pardir + "/"
    dirpath = "data/cifar-10-python.tar/cifar-10-batches-py/"
    file = "data_batch_1"
    fullpath = prjpath + dirpath + file
    dict = unpickle(fullpath)
    
    data = dict['data']
    labels = dict['labels'] 
    num = np.size(labels) #データ数

    ticktock = Ticktock.Ticktock()

    #参照色
#     ref_rgb = [25, 50, 100]
    ref_rgb = [0, 250, 0]

    # 一番色が近い画像を求める
    ticktock.tick()
    [minind, rss] = findNearestColorImage(dict, ref_rgb, range(1000))
#     [minind, rss] = findNearestColorImage(dict, ref_rgb)
    ticktock.tock()

    # 描画用に一番近い画像データを取得
    rgb = getRGBTable(dict, minind)
        
    # 描画
    ref_rgb3232 = np.ones([32,32,3], dtype='uint8') #imshowはuint8でなければ0..1に正規化しないといけないので明示的に書いとく。
    ref_rgb3232[:,:,:] = ref_rgb
    if True:
#         pl.clf()         
#         pl.ion()
        pl.subplot(2,1,1)
        pl.imshow(rgb, interpolation='none')
        pl.title('index: ' + str(minind) + ' \n RSS:' + str(rss))
#         pl.draw()
        pl.subplot(2,1,2)
        pl.imshow(ref_rgb3232, interpolation='none')
        pl.title('col:' + str(ref_rgb))
        pl.show()

 