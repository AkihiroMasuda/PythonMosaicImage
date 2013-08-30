# -*- coding: utf-8 -*-
'''
Created on 2013/08/29
png画像ファイルと numpyの配列 の相互変換サンプル
@author: akihiro
'''

import Image
import StringIO
import numpy as np
import matplotlib.pylab as pl

def convImgBindata2Array(data, fmt):
    img = Image.open(StringIO.StringIO(data))
    rgbimg = img.convert(fmt)
    rgb = np.array(rgbimg, dtype='uint8')
    return rgb

def convImgBindata2RGBAArray(data):
    return convImgBindata2Array(data, "RGBA")

def convImgBindata2RGBArray(data):
    return convImgBindata2Array(data, "RGB")


def convImgfile2RGBAArray(fname):
    f = open(fname, "rb")
    data = f.read()
    rgb = convImgBindata2RGBAArray(data)
    return rgb

def convRGBAArray2Imgfile(rgb_array, fname):
#     Image.save(rgb_array)
    pl.imsave(fname, rgb_array)

if __name__ == '__main__':
    rgb = convImgfile2RGBAArray('icon.png')
    print rgb
    print np.shape(rgb)
    convRGBAArray2Imgfile(np.reshape(rgb, [512,512,4]), 'hoge.png')
    pass