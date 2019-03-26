import os
import os.path
import pickle

import networkx as nx
import nltk
from nltk.corpus import wordnet as wn


def saveG(graph,path):
    pickle.dump(graph,open(path,'wb'))

def loadG(path):
    return pickle.load(open('path','rb'))

def nameN(node,type):
    if type == 'text':
        return 'text_%08d' % node
    elif type == 'keyword':
        return 'keyword_%s' % node
    elif type == 'entity':
        return 'entity_%s' % node[0]

def addTexts2G(G:nx.Graph,texts):
    for i,text in enumerate(texts):
        name = nameN(i,'text')
        print('Add Node <%s>' % name)
        G.add_node(name,type = 'text',text = text)

def addEntities2G(G:nx.Graph,entities):
    for entity in entities:
        name = nameN(entity,'entity')
        print('Add Node <%s>' % name)
        G.add_node(name,type = 'entity',entity = entity)

def addKeywords2G(G:nx.Graph,keywords):
    for keyword in keywords:
        name = nameN(keyword,'keyword')
        print('Add Node <%s>' % name)
        G.add_node(name,type = 'keyword',keyword = keyword)
    
def connectTextwithKeyword(G:nx.Graph,_keys):
    for k,ts in _keys.items():
        name_k = nameN(k,'keyword')
        for t in ts:
            name_t = nameN(t,'text')
            G.add_edge(name_k,name_t)
            print('Add Edge < %s , %s >...' % (name_k,name_t))

def connectTextwithEntity(G:nx.Graph,_entities):
    for e,ts in _entities.items():
        name_e = nameN(e,'entity')
        for t in ts:
            name_t = nameN(t,'text')
            G.add_edge(name_e,name_t)
            print('Add Edge < %s , %s >...' % (name_e,name_t))


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
    '''
    G = nx.Graph()
    addTexts2G(G,texts)
    addEntities2G(G,_entities.keys())
    addKeywords2G(G,_keys.keys())
    connectTextwithKeyword(G,_keys)
    connectTextwithEntity(G,_entities)
    pickle.dump(G,open(os.path.join(baseDir,'output','G-TEK-None.pkl'),'wb'))
    '''
    G = pickle.load(open(os.path.join(baseDir,'output','G-TEK-None.pkl'),'rb'))
    es = set()
    for e in _entities.keys():
        es.add(e[0])
    for e,rs in rels.items():
        for r in rs:
            if r in es:
                print('Add Edge < %s , %s >' % (nameN(e,'entity'),nameN((r,None),'entity')))
                G.add_edge(nameN(e,'entity'),nameN((r,None),'entity'))
            if r.lower() in _keys:
                print('Add Edge < %s , %s >' % (nameN(e,'entity'),nameN(r.lower(),'keyword')))
                G.add_edge(nameN(e,'entity'),nameN(r.lower(),'keyword'))
    
    for key in _keys.keys():
        for synset in wn.synsets(key):
            for word in synset.lemma_names():
                if word.lower() != key and word.lower() in _keys:
                    print('Add Edge < %s , %s >' % (nameN(key,'keyword'),nameN(word.lower(),'keyword'))))
                    G.add_edge(nameN(key,'keyword'),nameN(word.lower(),'keyword'))
    pickle.dump(G,open(os.path.join(baseDir,'output','G-TEK-EEEKKK.pkl'),'wb'))
