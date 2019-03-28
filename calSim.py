import networkx as nx
import pickle
import os
import os.path
import numpy as np

from concurrent.futures import ProcessPoolExecutor


def nameText(i):
    return 'text_%08d' % (i,)


def couP(G, s, t, prevs, path):
    if len(path) == 0:
        if t in G.adj[s]:
            return 1
        return 0
    ans = 0
    aim = path[0]
    adj = [node for node in G.adj[s] if node[:2]
           == aim[:2] and node not in prevs]
    for a in adj:
        ans += couP(G, a, t, prevs+[a], path[1:])
    return ans


def calAbyIndex(index, N, train_ids, G, paths):
    A = np.zeros((N, N))
    i = index+1
    for x in range(N):
        for y in range(0, x+1):
            tx, ty = nameText(train_ids[x]), nameText(train_ids[y])
            p = path[1:-1]
            print('Calculating CouP < path=%s , x=%s ,y=%s | total=%s >...' %
                  (i, tx, ty, N))
            c = couP(G, tx, ty, [], p)
            print('Get Coup(%s,%s)=%s.' % (x, y, c))
            A[i, x, y] = c
    np.save(os.path.join(baseDir, 'output', 'A-%s.pkl' % i), A)


if __name__ == "__main__":
    # baseDir = 'C:/Users/croxx/Desktop/rcv1'
    baseDir = '/home/LAB/penghao/croxx/HIN_PGCN'

    G = pickle.load(open(os.path.join(baseDir, 'output', 'G.pkl'), 'rb'))
    paths = [['text', 'entity', 'text'], ['text', 'keyword', 'text'], ['text', 'entity', 'entity', 'text'], ['text', 'entity', 'keyword', 'text'], ['text', 'keyword', 'entity', 'text'], ['text', 'keyword', 'keyword', 'text'], ['text', 'entity', 'entity', 'entity', 'text'], ['text', 'entity', 'entity', 'keyword', 'text'], [
        'text', 'entity', 'keyword', 'entity', 'text'], ['text', 'entity', 'keyword', 'keyword', 'text'], ['text', 'keyword', 'entity', 'entity', 'text'], ['text', 'keyword', 'entity', 'keyword', 'text'], ['text', 'keyword', 'keyword', 'entity', 'text'], ['text', 'keyword', 'keyword', 'keyword', 'text']]

    N = 23194
    '''
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
    '''
    train_ids = pickle.load(
        open(os.path.join(baseDir, 'output', 'train_ids.pkl'), 'rb'))

    executor = ProcessPoolExecutor(max_workers=20)
    for index, path in enumerate(paths):

    np.save(os.path.join(baseDir, 'output', 'A.pkl'), A)
    # pickle.dump(A, open(os.path.join(baseDir, 'output', 'A.pkl'), 'wb'))
