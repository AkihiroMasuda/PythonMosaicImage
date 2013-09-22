# -*- coding: utf-8 -*-
'''
Created on 2013/08/30

@author: akihiro
'''

import numpy 
import pickle
import os

def getPIXNUM():
    return 32

def getPIXSIZE():
    return getPIXNUM()**2

def getCifar10FilePath():
    if False:
        prjpath = "D:\\root\\programing\\Python\\MosaicImage\\" #絶対パスしていでないとインタラクティブモードで失敗する
        subdirpath = "data/cifar-10-python.tar/cifar-10-batches-py/"
        dirpath = prjpath + subdirpath
    else:
        dirpath = "/home/pi/ppdata/cifar-10/"
    file = "data_batch_1"
#     fullpath = prjpath + dirpath + file
    fullpath = dirpath + file
    return fullpath

def getMeanFilePath():
    '''
        画像毎の平均値を保存するファイルのパスを返す
    '''
    [dirpath, tail] = os.path.split(getCifar10FilePath())
    filename = "mean.dat"
    fullpath = dirpath + filename
    return fullpath

def isExistMenaFile():
    '''
        画像毎の平均値を保存したファイルｆが既にあるかどうかを返す
    '''
    return os.path.exists(getMeanFilePath())

def saveMeans(mean):
    '''
        画像毎の平均値をファイルに保存
    '''
    f = open(getMeanFilePath(), 'w');
    pickle.dump(mean, f)
    f.close()
    
def loadMeans():
    '''
        画像毎の平均値をファイルからロード
    '''
    f = open(getMeanFilePath());
    obj = pickle.load(f)
    f.close()
    return obj

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
    PIXSIZE = getPIXSIZE()
    r = curimg[0:PIXSIZE]
    g = curimg[PIXSIZE:PIXSIZE*2]
    b = curimg[PIXSIZE*2:]
    
    return r,g,b

def getImageNum(dict):
    '''
           画像 データ数を得る    
    '''
    labels = dict['labels']
    return numpy.size(labels)

def calMeans(dict):
    '''
    CIFAR-10画像データそれぞれの平均色を算出
    '''
    data = dict['data']
    num = getImageNum(dict)
    means = numpy.zeros([num, 3], 'uint8')
    for i in range(num):
        [r, g, b] = getRGB(dict, i)
        m_r = int(numpy.mean(r))
        m_g = int(numpy.mean(g))
        m_b = int(numpy.mean(b))
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
    rgb = numpy.vstack([r,g,b])
    PIXNUM = getPIXNUM()
    rgb = numpy.reshape(rgb.T, [PIXNUM, PIXNUM, 3])
    return rgb

def getColorRSSFromRGB(dict, index, ref_rgb):
    '''
    indexで指定した画像の ref_rgb との残差平方和RSSを求める
    '''
    [r, g, b] = getRGB(dict, index)
    m_r = ref_rgb[0]
    m_g = ref_rgb[1]
    m_b = ref_rgb[2]
    diff_r = numpy.mat(r,dtype='int')-m_r
    diff_g = numpy.mat(g,dtype='int')-m_g
    diff_b = numpy.mat(b,dtype='int')-m_b
    diff_rgb = numpy.vstack([diff_r, diff_g, diff_b])
    rss = numpy.sum(numpy.power(diff_rgb,2))
    return rss

def findNearestColorImage(dict, ref_rgb, indexes=None):
    '''
    ref_rgb との残差平方和RSSが最小の画像を探す
    '''
    if indexes==None:
        labels = dict['labels'] 
        num_all = numpy.size(labels) #データ数
        indexes = range(num_all)

    num = numpy.size(indexes)

    rsses = numpy.zeros(numpy.size(indexes), dtype="int")
#     for i in indexes:
    for i in range(num):
        # 参照色との残差平方和を求める
        rsses[i] = getColorRSSFromRGB(dict, indexes[i], ref_rgb)
        pass
    minind = numpy.argmin(rsses)
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
        num = numpy.size(labels) #データ数
        indexes = range(num)
    else :
        num = numpy.size(indexes)

    #平均色と指定色のRSS算出
    means_p = means[indexes, :]
    means_p_deff = means_p - numpy.ones([num, 1])*numpy.mat(ref_rgb)
    means_p_rss = numpy.sum(numpy.power(means_p_deff, 2),1) 
    
    #平均色のRSSをソート
    means_p_sort_indexes = numpy.argsort(means_p_rss.A1) #昇順
#     means_p_sort = numpy.sort(means_p_rss.A1)

    #画素毎のRSSによる評価対象とする数
    if num < num_threashold:
        num_threashold = num

    #平均色RSSの小さい上位nu_threasholdまでを抽出
    indexes_tar = numpy.array(indexes)[means_p_sort_indexes[:num_threashold]]

    #画素毎のRSSが小さい物を選ぶ
    return findNearestColorImage(dict, ref_rgb, indexes_tar)


def findNearestColorImageUseMeansOnly(dict, ref_rgb, means, indexes=None):
    '''
    ref_rgb 画像の平均色がもっとも近いものを採用。
    '''
    if indexes==None:
        labels = dict['labels'] 
        num = numpy.size(labels) #データ数
        indexes = range(num)
    else :
        num = numpy.size(indexes)

    #平均色と指定色のRSS算出
    means_p = means[indexes, :]
    means_p_deff = means_p - numpy.ones([num, 1])*numpy.mat(ref_rgb)
    means_p_rss = numpy.sum(numpy.power(means_p_deff, 2),1) 
    
    #平均色の残差が最小のものを選ぶ
    means_p_min_index = numpy.argmin(means_p_rss.A1) #最小のものを選択
    indexes_tar = numpy.array(indexes)[means_p_min_index]
    return indexes_tar, 0


def putSmallImageOntoLargeImage(largeImage, smallImage, x, y):
    '''
    smallImageをlargeImage上の座標x,yに配置する
    x,yにはsmallImageの左上が配置される
    '''
    xsize = numpy.shape(smallImage)[1]
    ysize = numpy.shape(smallImage)[0]
    largeImage[x:x+xsize, y:y+ysize, :] = smallImage


def makeMosaicImage(imgArray, numsOfSampleImages):
    dict = unpickle(getCifar10FilePath())
    
    data = dict['data']
    labels = dict['labels'] 
    num = numpy.size(labels) #データ数
    
    # 平均値一覧を取得
    if isExistMenaFile():
        means = loadMeans()
    else:
        means = calMeans(dict)
        saveMeans(means)

    range_xy = numpy.shape(imgArray)
    dest_image = numpy.zeros([range_xy[0]*32, range_xy[1]*32, 3], dtype='uint8') #uint8で作るのが大事
    for x in range(range_xy[0]):
#         print x
        for y in range(range_xy[1]):
            ref_rgb = imgArray[x,y,:]
            # 一番色が近い画像を求める
#             [minind2, rss2] = findNearestColorImage(dict, ref_rgb, range(100))
#             ind3 = range(100)
#             num_threashold=50
            num_threashold=1
#             [minind, rss] = findNearestColorImageUseMeans(dict, ref_rgb, means, num_threashold, range(10000))
#             [minind, rss] = findNearestColorImageUseMeans(dict, ref_rgb, means, num_threashold, range(100))
#             [minind, rss] = findNearestColorImageUseMeans(dict, ref_rgb, means, num_threashold, range(numsOfSampleImages))
            [minind, rss]  = findNearestColorImageUseMeansOnly(dict, ref_rgb, means, range(numsOfSampleImages))
            # 一番近い画像を取得
            near_rgb = getRGBTable(dict, minind)
            putSmallImageOntoLargeImage(dest_image, near_rgb, x*32, y*32)

    return dest_image


if __name__ == '__main__':
    pass