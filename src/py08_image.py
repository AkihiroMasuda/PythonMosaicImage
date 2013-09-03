# -*- coding: utf-8 -*-
'''
Created on 2013/08/29
png画像ファイルと numpyの配列 の相互変換サンプル
@author: akihiro
'''

# import Image
from PIL import Image
import StringIO
import numpy as np

def createImageFromBindata(data):
    return Image.open(StringIO.StringIO(data))

def convImg2Array(img, fmt):
    """
    input : img : Imageオブジェクト
            fmt : フォーマット  Image.mode参照
    return : 配列
            RGBの場合  MxNx3 [[[R00,G00,B00], [R01,G01,B01], ... ],
                           [[R10,G10,B10], [R11,G11,B11], ... ],
                           ...
                           ]
    """
    rgbimg = img.convert(fmt)
    rgb = np.array(rgbimg, dtype='uint8')
    return rgb

def convImgBindata2Array(data, fmt):
    img = Image.open(StringIO.StringIO(data))
    return convImg2Array(img, fmt)

def convImgBindata2RGBAArray(data):
    return convImgBindata2Array(data, "RGBA")

def convImgBindata2RGBArray(data):
    """
    return : RGB配列  MxNx3 [[[R00,G00,B00], [R01,G01,B01], ... ],
                           [[R10,G10,B10], [R11,G11,B11], ... ],
                           ...
                           ]
    """
    return convImgBindata2Array(data, "RGB")


def convImgfile2RGBAArray(fname):
    f = open(fname, "rb")
    data = f.read()
    rgb = convImgBindata2RGBAArray(data)
    return rgb

def convImgfile2RGBArray(fname):
    f = open(fname, "rb")
    data = f.read()
    rgb = convImgBindata2RGBArray(data)
    return rgb

def resizeImgBinData(data, size_x, size_y):
    img = Image.open(StringIO.StringIO(data))
    out_img = img.resize([size_x, size_y])
    return out_img

def convRGBAArray2Imgfile(rgb_array, fname):
    """
    numpy配列 からImageを使って保存
    """
    pilImg = Image.fromarray(np.uint8(rgb_array))
    pilImg.save(fname)
    

if __name__ == '__main__':
#     rgb = convImgfile2RGBAArray('icon.png')
    rgb = convImgfile2RGBArray('dest.png')
    print rgb
    print np.shape(rgb)
    size = np.shape(rgb)
    convRGBAArray2Imgfile(np.reshape(rgb, [size[0],size[1],3]), 'hoge.png')
    pass