# -*- coding: utf-8 -*-
'''
Created on 2013/08/23

@author: akihiro
'''
import numpy as np
import numpy.random as rnd
import matplotlib.pylab as pl
from numpy.random import * 
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

def getColorRSSFromRGB(dict, index, mean_rgb):
    '''
    indexで指定した画像の mean_rgb との残差平方和RSSを求める
    '''
    [r, g, b] = getRGB(dict, index)
    m_r = mean_rgb[0]
    m_g = mean_rgb[1]
    m_b = mean_rgb[2]
    diff_r = np.mat(r,dtype='int')-m_r
    diff_g = np.mat(g,dtype='int')-m_g
    diff_b = np.mat(b,dtype='int')-m_b
    diff_rgb = np.vstack([diff_r, diff_g, diff_b])
    rss = np.sum(np.power(diff_rgb,2))
    return rss


if __name__ == '__main__':
    [pardir, cur] =  os.path.split(os.path.dirname(__file__))
    prjpath = pardir + "/"
    dirpath = "data/cifar-10-python.tar/cifar-10-batches-py/"
    file = "data_batch_1"
    fullpath = prjpath + dirpath + file
    dict = unpickle(fullpath)
    
    data = dict['data']
    labels = dict['labels'] 
    
    num = np.size(labels) #データ数

    for i in range(10):
    
        # 指定画像のRGBを読み取り
        index = i
        rgb = getRGBTable(dict, index)
        ref_rgb = [0, 200, 0]
        rss = getColorRSSFromRGB(dict, index, ref_rgb)
        ref_rgb3232 = np.ones([32,32,3], dtype='uint8') #imshowはuint8でなければ0..1に正規化しないといけないので明示的に書いとく。
        ref_rgb3232[:,:,:] = ref_rgb
        print rss
        
        
        # 描画
#         pl.clf()         
#         pl.ion()
        pl.subplot(2,1,1)
        pl.imshow(rgb, interpolation='none')
        pl.title('RSS:' + str(rss))
#         pl.draw()
        pl.subplot(2,1,2)
        pl.imshow(ref_rgb3232, interpolation='none')
        pl.title('col:' + str(ref_rgb))
        pl.savefig(prjpath+"result/py02/" + str("%03d" % index) + ".png")
#         pl.show()
        
        pass    