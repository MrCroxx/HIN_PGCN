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


def getAHisName(t, history):
    name = t
    for h in history:
        name += '-%s' % h
    return name


def getANewName(t, history, tA, tB):
    name = t
    for h in history:
        name += '-%s' % h
    name += '-%s' % (tA+tB)
    return name


def martixMul(tA, tB, history):
    print('Calculating tA=%s,tB=%s,history=%s...' % (tA,tB,history))
    baseDir = '/home/LAB/penghao/croxx/HIN_PGCN'
    ALL = ['TT', 'EE', 'KK', 'TE', 'ET', 'TK', 'KT', 'EK', 'KE']
    tX00 = tA + tA
    tX01 = tA + tB
    tX10 = tB + tA
    tX11 = tB + tB
    for X in ALL:
        if X != tX00 and X != tX01 and X != tX10 and X != tX11:
            shutil.copyfile(getAFilename(baseDir,getAHisName(X,history)),getAFilename(baseDir,getANewName(X,history,tA,tB)))
    if tA != tB:
        X00 = np.mat(np.load(getAFilename(baseDir,getAHisName(tX00,history))))
        X01 = np.mat(np.load(getAFilename(baseDir,getAHisName(tX01,history))))
        X10 = np.mat(np.load(getAFilename(baseDir,getAHisName(tX10,history))))
        X11 = np.mat(np.load(getAFilename(baseDir,getAHisName(tX11,history))))
        nX00 = X00 * X00 + X01 * X10
        nX01 = X00 * X01 + X01 * X11
        nX10 = X10 * X00 + X11 * X10
        nX11 = X10 * X01 + X11 * X11
        np.save(getAPath(baseDir,getANewName(tX00,history,tA,tB)),nX00)
        np.save(getAPath(baseDir,getANewName(tX01,history,tA,tB)),nX01)
        np.save(getAPath(baseDir,getANewName(tX10,history,tA,tB)),nX10)
        np.save(getAPath(baseDir,getANewName(tX11,history,tA,tB)),nX11)
        del X00,X01,X10,X11,nX00,nX01,nX10,nX11
        gc.collect()
    if tA == tB:
        t = tA + tB
        X = np.mat(np.load(getAFilename(baseDir,getAHisName(t,history))))
        X = X * X
        np.save(getAPath(baseDir,getANewName(t,history,tA,tB)),X)
        del X
        gc.collect()



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

    calPath(paths[0])
