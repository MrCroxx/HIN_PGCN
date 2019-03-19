import os
import os.path
import pickle

import networkx as nx


def saveG(graph,path):
    pickle.dump(graph,open(path,'wb'))

def loadG(path):
    return pickle.load(open('path','rb'))

def addTexts2G(G:nx.Graph,texts):
    for i,text in enumerate(texts):
        name = 'text_%08d' % i
        print('Add Node <%s>' % name)
        G.add_node(name,text = text)

if __name__ == "__main__":
    # baseDir = 'C:/Users/croxx/Desktop/rcv1'
    baseDir = '/home/LAB/penghao/croxx/HIN'
    print('Loading texts...')
    texts = pickle.load(open(os.path.join(baseDir,'output','texts.pkl'),'rb'))
    print('Loading keys...')
    keys = pickle.load(open(os.path.join(baseDir,'output','keys.pkl'),'rb'))
    print('Loading entities...')
    entities = pickle.load(open(os.path.join(baseDir,'output','entities.pkl'),'rb'))
    print('Loading codes...')
    codes = pickle.load(open(os.path.join(baseDir,'output','codes.pkl'),'rb'))

    if len(texts) != len(keys) or len(texts) != len(entities) or len(texts) != len(codes):
        raise Exception('Lengths of texts,keys,entities and codes should be the same.')
    

    G = nx.Graph()
    addTexts2G(G,texts)
    
