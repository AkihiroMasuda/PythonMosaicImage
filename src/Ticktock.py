# -*- coding: utf-8 -*-
'''
Created on 2013/08/23

@author: akihiro
'''
import time

class Ticktock(object):
    def __init__(self):
        self.ticktime = 0
        self.tockltime = 0
    
    def tick(self):
        self.ticktime = time.time()
    
    def tock(self):
        self.tocktime = time.time()
        print "測定時間:" + str(self.tocktime-self.ticktime) + "[s]"