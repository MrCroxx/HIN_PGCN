import networkx as nx
import pickle
import os
import os.path


def createCodeG(f_hier):
    rows = f_hier.readlines()
    CG = nx.Graph()
    for row in rows:
        info = row.split()
        p, c = info[1], info[3]
        CG.add_edge(p, c)
    return CG


if __name__ == "__main__":
    baseDir = 'D:/Lab/HIN_PGCN'
    # baseDir = '/home/LAB/penghao/croxx/HIN_PGCN'
    f_hier = open(os.path.join(baseDir, 'files',
                               'rcv1.topics.hier.orig.txt'), 'r', encoding='utf8')
    codes = pickle.load(open(os.path.join(baseDir,'output','codes.pkl'),'rb'))
    CG = createCodeG(f_hier)
    ds = dict(nx.all_pairs_shortest_path_length(CG))
    train_ids = pickle.load(open(os.path.join(baseDir,'output','train_ids.pkl'),'rb'))

    sims = {}
    for x in train_ids:
        for y in train_ids:
            if (x,y) in sims:
                continue
            cx = set(codes[x].split())
            cy = set(codes[y].split())
            sim = (len(cx & cy)*2)
            for c1 in cx:
                for c2 in cy:
                    if ds[c1][c2] == 1:
                        sim += 0.2
                    elif ds[c1][c2] == 2:
                        sim += 0.1
            sim /= ( len(cx) + len(cy) )
            if sim > 1:
                sim = 1
            sims[(x,y)] = sims[(y,x)] = sim
            print('Sim(%s,%s) = %s' %(x,y,sim))
    pickle.dump(sims,open(os.path.join(baseDir,'output','sims.pkl'),'wb'))
