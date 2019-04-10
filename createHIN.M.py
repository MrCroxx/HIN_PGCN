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

if __name__ == "__main__":
    # baseDir = 'C:/Users/croxx/Desktop/rcv1'
    baseDir = '/home/LAB/penghao/croxx/HIN_PGCN'
    
    print('Loading texts...')
    texts = pickle.load(open(os.path.join(baseDir,'output','texts.pkl'),'rb'))
    print('Loading _keys...')
    _keys = pickle.load(open(os.path.join(baseDir,'output','_keys.pkl'),'rb'))
    print('Loading _entities...')
    _entities = pickle.load(open(os.path.join(baseDir,'output','_entities.pkl'),'rb'))
    print('Loading rels...')
    rels = pickle.load(open(os.path.join(baseDir,'output','rels.pkl'),'rb'))

    N = 23194
    ntext = len(texts)
    nentity = len(_entities)
    nkey = len(_keys)

    types = ['T','E','K']

    '''

    edges = {}
    for i in types:
        for j in types:
            edges[(i,j)] = []
    
    key2id = {}
    entity2id = {}

    for i,k in enumerate(_keys.keys()):
        key2id[k] = i
    
    for i,k in enumerate(_entities.keys()):
        e = k[0]
        entity2id[e] = i
    
    print('Mapping keywords and entities...')
    pickle.dump(key2id,open(os.path.join(baseDir,'output','key2id.pkl'),'wb'))
    pickle.dump(entity2id,open(os.path.join(baseDir,'output','entity2id.pkl'),'wb'))
    print('Finish mapping keywords and entities.')
    '''

    
    '''
    print('Picking train set...')
    train_ids = []
    _cs = pickle.load(
        open(os.path.join(baseDir, 'output', '_codes.pkl'), 'rb'))

    while len(train_ids) < N:
        for c, ts in _cs.items():
            if len(ts) == 0:
                continue
            while ts[0] in train_ids:
                del ts[0]
            train_ids.append(ts[0])
            print('add train id %s' % ts[0])
            del ts[0]

    train_ids = sorted(train_ids)
    for i in train_ids:
        print('train id %s' % i)
    pickle.dump(train_ids, open(os.path.join(baseDir, 'output', 'train_ids.pkl'),'wb'))
    print('Finish picking train set.')
    '''
    '''
    train_ids = pickle.load(open(os.path.join(baseDir,'output','train_ids.pkl'),'rb'))
    
    for e,tids in _entities.items():
        e = e[0]
        eid = entity2id[e]
        for tid in tids:
            edges[('E','T')].append((eid,tid))
            edges[('T','E')].append((tid,eid))

    for k,tids in _keys.items():
        kid = key2id[k]
        for tid in tids:
            edges[('K','T')].append((kid,tid))
            edges[('T','K')].append((tid,kid))
        

    for e,rs in rels.items():
        for r in rs:
            if e in entity2id and r in entity2id:
                edges[('E','E')].append((entity2id[e],entity2id[r]))
                edges[('E','E')].append((entity2id[r],entity2id[e]))
            if e in entity2id and r.lower() in key2id:
                edges[('E','K')].append((entity2id[e],key2id[r.lower()]))
                edges[('K','E')].append((key2id[r.lower()],entity2id[e]))

    for key in _keys.keys():
        for synset in wn.synsets(key):
            for word in synset.lemma_names():
                if word.lower() != key and word.lower() in key2id:
                    edges[('K','K')].append((key2id[key],key2id[word.lower()]))
                    edges[('K','K')].append((key2id[word.lower()],key2id[key]))
    
    pickle.dump(edges,open(os.path.join(baseDir,'output','edges.pkl'),'wb'))

    '''
    # Create and Save Initial A matrix.

    edges = pickle.load(open(os.path.join(baseDir,'output','edges.pkl'),'rb'))
    train_ids = pickle.load(open(os.path.join(baseDir,'output','train_ids.pkl'),'rb'))

    tid2index = { tid:index for index,tid in enumerate(train_ids) }


    print('Creating TT...')
    TT = np.zeros((N,N))
    np.save(getAPath(baseDir,'TT'),TT)
    del TT
    gc.collect()

    print('Creating EE...')
    EE = np.zeros((nentity,nentity))
    for pair in edges[('E','E')]:
        x, y = pair
        EE[x,y] = 1
    np.save(getAPath(baseDir,'EE'),EE)
    del EE
    gc.collect()

    print('Creating KK...')
    KK = np.zeros((nkey,nkey))
    for pair in edges[('K','K')]:
        x, y = pair
        KK[x,y] = 1
    np.save(getAPath(baseDir,'KK'),KK)
    del KK
    gc.collect()

    print('Creating TE...')
    TE = np.zeros((N,nentity))
    for pair in edges[('T','E')]:
        x, y = pair
        x = tid2index[x]
        TE[x,y] = 1
    np.save(getAPath(baseDir,'TE'),TE)
    del TE
    gc.collect()

    print('Creating ET...')
    ET = np.zeros((nentity,N))
    for pair in edges[('E','T')]:
        x, y = pair
        y = tid2index[y]
        ET[x,y] = 1
    np.save(getAPath(baseDir,'ET'),ET)
    del ET
    gc.collect()

    print('Creating TK...')
    TK = np.zeros((N,nkey))
    for pair in edges[('T','K')]:
        x, y = pair
        x = tid2index[x]
        TK[x,y] = 1
    np.save(getAPath(baseDir,'TK'),TK)
    del TK
    gc.collect()

    print('Creating KT...')
    KT = np.zeros((nkey,N))
    for pair in edges[('K','T')]:
        x, y = pair
        y = tid2index[y]
        KT[x,y] = 1
    np.save(getAPath(baseDir,'KT'),KT)
    del KT
    gc.collect()

    print('Creating EK...')
    EK = np.zeros((nentity,nkey))
    for pair in edges[('E','K')]:
        x, y = pair
        EK[x,y] = 1
    np.save(getAPath(baseDir,'EK'),EK)
    del EK
    gc.collect()
    
    print('Creating KE...')
    KE = np.zeros((nkey,nentity))
    for pair in edges[('K','E')]:
        x, y = pair
        KE[x,y] = 1
    np.save(getAPath(baseDir,'KE'),KE)
    del KE
    gc.collect()