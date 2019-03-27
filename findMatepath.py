import pickle
import networkx as nx 
import os
from os.path import exists,join

if __name__ == "__main__":
    # baseDir = '/home/LAB/penghao/croxx/HIN_PGCN'
    baseDir = 'D:\\Lab\\HIN_PGCN'

    G = pickle.load(open(join(baseDir,'G.pkl'),'rb'))
    es = []
    ps = []
    for node in G.nodes:
        if node[:2] == 'en':
            es.append(node)
    for e in es:
        for a in G.adj[e]:
            if a[:2] == 'en':
                ps.append((e,a))
    for px,py in ps:
        print('Finding in < %s , %s >' % (px,py))
        for n1 in G.adj[px]:
            for n2 in G.adj[py]:
                if n1[:2] == 'te' and n2[:2] == 'te' and n1!=n2:
                    print(n1,px,py,n2,'Bingo !!')


    