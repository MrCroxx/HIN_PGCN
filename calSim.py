import networkx as nx
import pickle
import os
import os.path
import numpy as np


def nameText(index):
    # index means index in numpy martix, not the id of the text
    return 'text_%08d' % (index-1)


def couP(G, s, t, path):
    if len(path) == 0:
        if t in G.adj[s]:
            return 1
        return 0
    ans = 0
    aim = path[0]
    adj = [ node for node in G.adj[s] if node[:2] == aim[:2] ]
    for a in adj:
        ans += couP(G,a,t,path[1:])
    return ans




if __name__ == "__main__":
    # baseDir = 'C:/Users/croxx/Desktop/rcv1'
    baseDir = '/home/LAB/penghao/croxx/HIN_PGCN'

    G = pickle.load(open(os.path.join(baseDir, 'output', 'G.pkl'), 'rb'))
    paths = [['text', 'entity', 'text'], ['text', 'keyword', 'text'], ['text', 'entity', 'entity', 'text'], ['text', 'entity', 'keyword', 'text'], ['text', 'keyword', 'entity', 'text'], ['text', 'keyword', 'keyword', 'text'], ['text', 'entity', 'entity', 'entity', 'text'], ['text', 'entity', 'entity', 'keyword', 'text'], [
        'text', 'entity', 'keyword', 'entity', 'text'], ['text', 'entity', 'keyword', 'keyword', 'text'], ['text', 'keyword', 'entity', 'entity', 'text'], ['text', 'keyword', 'entity', 'keyword', 'text'], ['text', 'keyword', 'keyword', 'entity', 'text'], ['text', 'keyword', 'keyword', 'keyword', 'text']]
    '''
    ts = []
    es = []
    ks = []

    for node in G.nodes:
        if node[:2] == 'te':
            ts.append(node)
        elif node[:2] == 'en':
            es.append(node)
        elif node[:2] == 'ke':
            ks.append(node)
    '''
    '''
    ts = set()
    es = set()
    ks = set()

    for node in G.nodes:
        if node[:2] == 'te':
            ts.add(node)
        elif node[:2] == 'en':
            es.add(node)
        elif node[:2] == 'ke':
            ks.add(node)
    '''

    N = len(ts)
    A = np.zeros((14, N, N))
    for index, path in enumerate(paths):
        i = index+1
        for x in range(1, N+1):
            for y in range(1, x+1):
                p = path[1:-1]
                print('Calculating CouP < path=%s , x=%s ,y=%s | total=%s >...' % (i,x,y,N))
                c = couP(G, nameText(x), nameText(y), p)
    pickle.dump(A,open(os.path.join(baseDir,'output','A-half.pkl'),'wb'))