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

    for i,key in enumerate(keys_raw):
        print('Processing key %s...' % i)
        if key not in keys:
            keys[key] = set()
        keys[key].append(i)

    for i,entity in enumerate(entities_raw):        
        print('Processing entity %s...' % i)
        if entity not in entities:
            entities[entity] = set()
        entities[entity].append(i)

    for i,code in enumerate(codes_raw):
        print('Processing code %s...' % i)
        if code not in codes:
            codes[code] = set()
        codes[code].append(i)

    pickle.dump(keys,open(os.path.join(baseDir,'output','_keys.pkl'),'wb'))
    pickle.dump(entities,open(os.path.join(baseDir,'output','_entitis.pkl'),'wb'))
    pickle.dump(codes,open(os.path.join(baseDir,'output','_codes.pkl'),'wb'))
    