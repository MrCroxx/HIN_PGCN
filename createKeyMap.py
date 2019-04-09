import os
import os.path
import pickle

if __name__ == "__main__":
    # baseDir = 'D:/Lab/HIN_PGCN'
    baseDir = '/home/LAB/penghao/croxx/HIN_PGCN'

    keys = {}
    entities = {}
    codes = {}


    print('Loading keys...')
    keys_raw = pickle.load(open(os.path.join(baseDir,'output','keys.pkl'),'rb'))
    print('Loading entities...')
    entities_raw = pickle.load(open(os.path.join(baseDir,'output','entities.pkl'),'rb'))
    print('Loading codes...')
    codes_raw = pickle.load(open(os.path.join(baseDir,'output','codes.pkl'),'rb'))

    for i,row in enumerate(keys_raw):
        print('Processing key %s...' % i)
        for key in row[:5]:
            if key not in keys:
                keys[key] = []
            keys[key].append(i)

    for i,row in enumerate(entities_raw):        
        print('Processing entity %s...' % i)
        for entity in row[:5]:
            if entity not in entities:
                entities[entity] = []
            entities[entity].append(i)

    for i,row in enumerate(codes_raw):
        print('Processing code %s...' % i)
        for code in row:
            if code not in codes:
                codes[code] = []
            codes[code].append(i)

    pickle.dump(keys,open(os.path.join(baseDir,'output','_keys.pkl'),'wb'))
    pickle.dump(entities,open(os.path.join(baseDir,'output','_entities.pkl'),'wb'))
    pickle.dump(codes,open(os.path.join(baseDir,'output','_codes.pkl'),'wb'))
    