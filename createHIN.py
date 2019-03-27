import os
import os.path
import pickle

import networkx as nx
import nltk
from nltk.corpus import wordnet as wn


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
                n1,n2 = nameN(e,'entity'),nameN((r,None),'entity')
                if n1 in G.nodes and n2 in G.nodes:
                    print('Add Edge < %s , %s >' % (nameN(e,'entity'),nameN((r,None),'entity')))
                    G.add_edge(nameN(e,'entity'),nameN((r,None),'entity'))
                else:
                    print('No Edge < %s , %s >' % (nameN(e,'entity'),nameN((r,None),'entity')))
            if r.lower() in _keys:
                n1,n2 = nameN(e,'entity'),nameN(r.lower(),'keyword')
                if n1 in G.nodes and n2 in G.nodes:
                    print('Add Edge < %s , %s >' % (nameN(e,'entity'),nameN(r.lower(),'keyword')))
                    G.add_edge(nameN(e,'entity'),nameN(r.lower(),'keyword'))
                else:
                    print('No Edge < %s , %s >' % (nameN(e,'entity'),nameN(r.lower(),'keyword'))
    
    for key in _keys.keys():
        for synset in wn.synsets(key):
            for word in synset.lemma_names():
                if word.lower() != key and word.lower() in _keys:
                    n1,n2 = nameN(key,'keyword'),nameN(word.lower(),'keyword')
                    if n1 in G.nodes and n2 in G.nodes:
                        print('Add Edge < %s , %s >' % (nameN(key,'keyword'),nameN(word.lower(),'keyword')))
                        G.add_edge(nameN(key,'keyword'),nameN(word.lower(),'keyword'))
                    else:
                        print('No Edge < %s , %s >' % (nameN(key,'keyword'),nameN(word.lower(),'keyword'))
    pickle.dump(G,open(os.path.join(baseDir,'output','G-TEK-EEEKKK.pkl'),'wb'))
    
    '''
    ps = {}
    paths = [['text', 'entity', 'text'], ['text', 'keyword', 'text'], ['text', 'entity', 'entity', 'text'], ['text', 'entity', 'keyword', 'text'], ['text', 'keyword', 'entity', 'text'], ['text', 'keyword', 'keyword', 'text'], ['text', 'entity', 'entity', 'entity', 'text'], ['text', 'entity', 'entity', 'keyword', 'text'], [
        'text', 'entity', 'keyword', 'entity', 'text'], ['text', 'entity', 'keyword', 'keyword', 'text'], ['text', 'keyword', 'entity', 'entity', 'text'], ['text', 'keyword', 'entity', 'keyword', 'text'], ['text', 'keyword', 'keyword', 'entity', 'text'], ['text', 'keyword', 'keyword', 'keyword', 'text']]
    G = pickle.load(
        open(os.path.join(baseDir, 'output', 'G-TEK-EEEKKK.pkl'), 'rb'))
    for p in paths:
        print('Finding Path : ', p, ' ...')
        ans = findPath(G, p)
        if ans is not None:
            print('Path Found : ', p, '\n', '------->', ans)
            ps[str(p)] = ans
    pickle.dump(ps, open(os.path.join(
        baseDir, 'output', 'matepaths.pkl'), 'rb'))
    '''