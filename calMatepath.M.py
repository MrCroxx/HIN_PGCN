import os
import os.path
import pickle

import networkx as nx
import nltk
import numpy as np
from nltk.corpus import wordnet as wn
import gc
import shutil


def getAPath(baseDir, name):
    return os.path.join(baseDir, 'output', 'A', name)

def getAFilename(baseDir,name):
    return os.path.join(baseDir, 'output', 'A', '%s.npy' % name)


def getAHisName(X, history):
    name = X
    for h in history:
        name += '-%s' % h
    return name


def getANewName(X, history, tA, tB):
    name = X
    for h in history:
        name += '-%s' % h
    name += '-%s' % (tA+tB)
    return name


def martixMul(tA, tB, history):
    baseDir = '/home/LAB/penghao/croxx/HIN_PGCN'
    ALL = ['TT', 'EE', 'KK', 'TE', 'ET', 'TK', 'KT', 'EK', 'KE']
    X00 = tA + tA
    X01 = tA + tB
    X10 = tB + tA
    X11 = tB + tB
    for X in ALL:
        if X != X00 and X != X01 and X != X10 and X != X11:
            shutil.copyfile(getAFilename(baseDir,getAHisName(X,history)),getAFilename(baseDir,getANewName(X,history,tA,tB)))
    if tA != tB:
        pass
    if tA == tB:
        t = tA + tB
        X = np.load(getAFilename(baseDir,getAHisName(t,history)))
        


def calPath(path):
    pstr = ''.join(path)
    history = []
    for i in range(len(path)-1):
        j = i + 1
        martixMul(path[i], path[j], history)
        history.append(path[i]+path[j])


if __name__ == "__main__":
    # baseDir = 'C:/Users/croxx/Desktop/rcv1'
    baseDir = '/home/LAB/penghao/croxx/HIN_PGCN'

    nums = pickle.load(open(os.path.join(baseDir, 'output', 'nums.pkl'), 'rb'))

    N = nums['N']
    ntext = nums['ntext']
    nentity = nums['nentity']
    nkey = nums['nkey']

    types = ['T', 'E', 'K']

    paths = [['T', 'E', 'T'], ['T', 'K', 'T'], ['T', 'E', 'E', 'T'], ['T', 'E', 'K', 'T'], ['T', 'K', 'E', 'T'], ['T', 'K', 'K', 'T'], ['T', 'E', 'E', 'E', 'T'], ['T', 'E', 'E', 'K', 'T'], [
        'T', 'E', 'K', 'E', 'T'], ['T', 'E', 'K', 'K', 'T'], ['T', 'K', 'E', 'E', 'T'], ['T', 'K', 'E', 'K', 'T'], ['T', 'K', 'K', 'E', 'T'], ['T', 'K', 'K', 'K', 'T']]

    train_ids = pickle.load(
        open(os.path.join(baseDir, 'output', 'train_ids.pkl'), 'rb'))
    tid2index = {tid: index for index, tid in enumerate(train_ids)}
