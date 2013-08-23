# -*- coding: utf-8 -*-
'''
Created on 2013/08/23
@author: akihiro
CIFAR-10画像を読み込む
'''
import numpy as np
import numpy.random as rnd
import matplotlib.pylab as pl
from numpy.random import * 
import time
import os, sys


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
    '''
        ロードしたdictから指定インデックスのRGB配列(32x32x3)を得る。
    [[p0_r, p0_g, p0_b], [p1_r, p1_g, p1_b], ..., [p31_r, p31_g, p31_b]],
    [[p32_r, p32_g, p32_b],                  ...,                      ],
    ]
    '''
    data = dict['data']
    labels = dict['labels'] 
    datanum = np.shape(data)
    pixnum = 32
    pixsize = pixnum*pixnum 
    
    curimg = data[index]
    r = curimg[0:pixsize]
    g = curimg[pixsize:pixsize*2]
    b = curimg[pixsize*2:]
    
    rgb = np.vstack([r,g,b])
    rgb = np.reshape(rgb.T, [pixnum, pixnum, 3])
    return rgb

if __name__ == '__main__':
    [pardir, cur] =  os.path.split(os.path.dirname(__file__))
    prjpath = pardir + "/"
    dirpath = "data/cifar-10-python.tar/cifar-10-batches-py/"
    file = "data_batch_1"
    fullpath = prjpath + dirpath + file
    dict = unpickle(fullpath)
    
    data = dict['data']
    labels = dict['labels'] 

    for i in range(10):
    
        # 指定画像のRGBを読み取り
        index = i
        rgb = getRGB(dict, index)
    
        # 描画
        pl.clf()         
        pl.ion()
        pl.imshow(rgb, interpolation='none')
        pl.title('label:' + str(labels[index]))
        pl.draw()
        
        pass    