import os,time
import os.path
import pickle
import re
from concurrent.futures import ProcessPoolExecutor, as_completed

import nltk
import nltk.corpus


def loadStops(path: str):
    stops = set()
    with open(path, 'r', encoding='utf8') as f:
        rows = f.readlines()
        for row in rows:
            stops.add(row[:-1])
    return stops

def containsAlphaOrNumber(s: str, reprog):
    return reprog.search(s) is not None

def removeStopsAndNonEn(tree, stops: set,reprog):
    entities = []
    if isinstance(tree[0],str):
        lower = tree[0].lower()
        if containsAlphaOrNumber(lower,reprog) and lower not in stops:
            entities.append(tree)
    else:
        for node in tree:
            entities += removeStopsAndNonEn(node,stops,reprog)
    return entities

def extractEntities(args):
    i,text,stops,reprog = args
    tokens = nltk.word_tokenize(text)
    tokens = nltk.pos_tag(tokens)
    tree = nltk.ne_chunk(tokens)
    en = removeStopsAndNonEn(tree,stops,reprog)
    print('Finish extracting text %s.' % i)
    return en

if __name__ == "__main__":
    
    baseDir = 'C:/Users/croxx/Desktop/rcv1'
    # baseDir = '/home/LAB/penghao/croxx/HIN'
    stops = loadStops(os.path.join(baseDir, 'files/english.stop.txt'))
    texts = pickle.load(open(os.path.join(baseDir,'output','text.pkl'),'rb'))
    # texts = texts[:100]
    reprog = re.compile(r'[a-z]')
    ens = [ None for i in range(len(texts)) ]

    executor = ProcessPoolExecutor(max_workers=8)
    tasks = [ executor.submit(extractEntities,args=(i,text,stops,reprog)) for i,text in enumerate(texts) ]
    ens = [ task.result() for task in as_completed(tasks) ]
    pickle.dump(ens,open(os.path.join(baseDir,'output','entities.pkl'),'wb'))