import os
import os.path
import pickle

import networkx as nx
import nltk
import numpy as np
from nltk.corpus import wordnet as wn
import gc

def getAPath(baseDir,name):
    return os.path.join(baseDir,'output','A',name)

def martixMul(tA,tB,history):
    ALL = ['TT','EE','KK','TE','ET','TK','KT','EK','KE']
    X00 = tA + tA
    X01 = tA + tB
    X10 = tB + tA
    X11 = tB + tB
    for X in ALL:
        if X != X00 and X != X01 and X != X10 and X != X11:
            pass
    if tA != tB:
        pass
    if tA == tB:
        pass

if __name__ == "__main__":
    # baseDir = 'C:/Users/croxx/Desktop/rcv1'
    baseDir = '/home/LAB/penghao/croxx/HIN_PGCN'
    
    nums = pickle.load(open(os.path.join(baseDir,'output','nums.pkl'),'rb'))

    N = nums['N']
    ntext = nums['ntext']
    nentity = nums['nentity']
    nkey = nums['nkey']

    types = ['T','E','K']
    
    
    train_ids = pickle.load(open(os.path.join(baseDir,'output','train_ids.pkl'),'rb'))
    tid2index = { tid:index for index,tid in enumerate(train_ids) }