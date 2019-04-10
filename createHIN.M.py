import os
import os.path
import pickle

import networkx as nx
import nltk
from nltk.corpus import wordnet as wn
import numpy as np


def saveG(graph, path):
    pickle.dump(graph, open(path, 'wb'))


def loadG(path):
    return pickle.load(open('path', 'rb'))


def nameN(node, type):
    if type == 'text':
        return 'text_%08d' % node
    elif type == 'keyword':
        return 'keyword_%s' % node
    elif type == 'entity':
        return 'entity_%s' % node[0]


def addTexts2G(G: nx.Graph, texts):
    for i, text in enumerate(texts):
        name = nameN(i, 'text')
        print('Add Node <%s>' % name)
        G.add_node(name, type='text', text=text)


def addEntities2G(G: nx.Graph, entities):
    for entity in entities:
        name = nameN(entity, 'entity')
        print('Add Node <%s>' % name)
        G.add_node(name, type='entity', entity=entity)


def addKeywords2G(G: nx.Graph, keywords):
    for keyword in keywords:
        name = nameN(keyword, 'keyword')
        print('Add Node <%s>' % name)
        G.add_node(name, type='keyword', keyword=keyword)


def connectTextwithKeyword(G: nx.Graph, _keys):
    for k, ts in _keys.items():
        name_k = nameN(k, 'keyword')
        for t in ts:
            name_t = nameN(t, 'text')
            G.add_edge(name_k, name_t)
            print('Add Edge < %s , %s >...' % (name_k, name_t))


def connectTextwithEntity(G: nx.Graph, _entities):
    for e, ts in _entities.items():
        name_e = nameN(e, 'entity')
        for t in ts:
            name_t = nameN(t, 'text')
            G.add_edge(name_e, name_t)
            print('Add Edge < %s , %s >...' % (name_e, name_t))


def findNext(G, n, pp, pn):
    if len(pn) == 0:
        return pp
    for node in G.adj[n]:
        if node[:2] == pn[0][:2] and node not in pp:
            return findNext(G, node, pp + [node], pn[1:])
    return None


def findPath(G, p):
    ans = None
    for s in G.nodes:
        if ans is not None:
            return ans
        if s[:2] == 'te':
            ans = findNext(G, s, [s], p[1:])
    return ans


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

    ntext = len(texts)
    nentity = len(_entities)
    nkey = len(_keys)

    types = ['T','E','K']

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


    N = 23194
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
            if r.lower() in key2id:
                edges[('E','K')].append((entity2id[r],key2id[r.lower()]))
                edges[('K','E')].append((key2id[r.lower()],entity2id[r]))

    for key in _keys.keys():
        for synset in wn.synsets(key):
            for word in synset.lemma_names():
                if word.lower() != key and word.lower() in key2id:
                    edges[('K','K')].append((key2id[key],key2id[word.lower()]))
                    edges[('K','K')].append((key2id[word.lower()],key2id[key]))
    
    pickle.dump(edges,open(os.path.join(baseDir,'output','edges.pkl'),'wb'))


    '''
    G = nx.Graph()
    addTexts2G(G,texts)
    addEntities2G(G,_entities.keys())
    addKeywords2G(G,_keys.keys())
    connectTextwithKeyword(G,_keys)
    connectTextwithEntity(G,_entities)
    pickle.dump(G,open(os.path.join(baseDir,'output','G-TEK-None.pkl'),'wb'))
    
    
    G = pickle.load(open(os.path.join(baseDir,'output','G-TEK-None.pkl'),'rb'))
    es = set()
    for e in _entities.keys():
        es.add(e[0])
    for e,rs in rels.items():
        for r in rs:
            if r in es:
                n1,n2 = nameN((e,None),'entity'),nameN((r,None),'entity')
                if n1 in G.nodes and n2 in G.nodes:
                    print('Add Edge < %s , %s >' % (nameN((e,None),'entity'),nameN((r,None),'entity')))
                    G.add_edge(nameN((e,None),'entity'),nameN((r,None),'entity'))
                else:
                    print('No Edge < %s , %s >' % (nameN((e,None),'entity'),nameN((r,None),'entity')))
            if r.lower() in _keys:
                n1,n2 = nameN((e,None),'entity'),nameN(r.lower(),'keyword')
                if n1 in G.nodes and n2 in G.nodes:
                    print('Add Edge < %s , %s >' % (nameN((e,None),'entity'),nameN(r.lower(),'keyword')))
                    G.add_edge(nameN((e,None),'entity'),nameN(r.lower(),'keyword'))
                else:
                    print('No Edge < %s , %s >' % (nameN((e,None),'entity'),nameN(r.lower(),'keyword')))
    
    for key in _keys.keys():
        for synset in wn.synsets(key):
            for word in synset.lemma_names():
                if word.lower() != key and word.lower() in _keys:
                    n1,n2 = nameN(key,'keyword'),nameN(word.lower(),'keyword')
                    if n1 in G.nodes and n2 in G.nodes:
                        print('Add Edge < %s , %s >' % (nameN(key,'keyword'),nameN(word.lower(),'keyword')))
                        G.add_edge(nameN(key,'keyword'),nameN(word.lower(),'keyword'))
                    else:
                        print('No Edge < %s , %s >' % (nameN(key,'keyword'),nameN(word.lower(),'keyword')))
    pickle.dump(G,open(os.path.join(baseDir,'output','G.pkl'),'wb'))
    '''

    