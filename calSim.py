import networkx as nx
import pickle
import os
import os.path
import numpy as np


def nameText(i):
    return 'text_%08d' % (i,)


def couP(G, s, t, path):
    if len(path) == 0:
        if t in G.adj[s]:
            return 1
        return 0
    ans = 0
    aim = path[0]
    adj = [node for node in G.adj[s] if node[:2] == aim[:2]]
    for a in adj:
        ans += couP(G, a, t, path[1:])
    return ans


if __name__ == "__main__":
    # baseDir = 'C:/Users/croxx/Desktop/rcv1'
    baseDir = '/home/LAB/penghao/croxx/HIN_PGCN'

    G = pickle.load(open(os.path.join(baseDir, 'output', 'G.pkl'), 'rb'))
    paths = [['text', 'entity', 'text'], ['text', 'keyword', 'text'], ['text', 'entity', 'entity', 'text'], ['text', 'entity', 'keyword', 'text'], ['text', 'keyword', 'entity', 'text'], ['text', 'keyword', 'keyword', 'text'], ['text', 'entity', 'entity', 'entity', 'text'], ['text', 'entity', 'entity', 'keyword', 'text'], [
        'text', 'entity', 'keyword', 'entity', 'text'], ['text', 'entity', 'keyword', 'keyword', 'text'], ['text', 'keyword', 'entity', 'entity', 'text'], ['text', 'keyword', 'entity', 'keyword', 'text'], ['text', 'keyword', 'keyword', 'entity', 'text'], ['text', 'keyword', 'keyword', 'keyword', 'text']]

    N = 23194
    train_ids = []

    _cs = pickle.load(
        open(os.path.join(baseDir, 'output', '_codes.pkl'), 'rb'))

    for c, ts in _cs:
        if len(train_ids) < N:
            train_ids.append(ts[0])
            del ts[0]

    train_ids = sorted(train_ids)
    print(train_ids)
    pickle.dump(train_ids, os.path.join(baseDir, 'output', 'train_ids.pkl'))

    A = np.zeros((14, N, N))
    for index, path in enumerate(paths):
        i = index+1
        for x in range(N):
            for y in range(0, x+1):
                tx, ty = nameText(train_ids(x)), nameText(train_ids(y))
                p = path[1:-1]
                print('Calculating CouP < path=%s , x=%s ,y=%s | total=%s >...' % (
                    i, tx, ty, N))
                c = couP(G, tx, ty, p)
                print('Get Coup(%s,%s)=%s.' % (x, y, c))
                A[i, x, y] = c
    pickle.dump(A, open(os.path.join(baseDir, 'output', 'A.pkl'), 'wb'))
