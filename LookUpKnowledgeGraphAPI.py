import json
import os
import os.path
import pickle
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests


def lookup(args):
    query, api_key = args
    # print('Looking up <%s>...' % (query,))
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    params = {
        'query': query,
        'limit': 100,
        'indent': True,
        'key': api_key,
    }
    proxies = {
        "http": "socks5://10.111.2.130:1080",
        'https': 'socks5://10.111.2.130:1080'
    }
    ans = []
    try:
        res = requests.get(service_url, params=params, proxies=proxies)
        # res = requests.get(service_url, params=params)
        if res.status_code != 200:
            print('Fail')
            return query
        j = json.loads(res.text)

        for element in j['itemListElement']:
            if 'result' in element:
                if 'name' in element['result']:
                    ans.append(element['result']['name'])
        print('Lookup <%s> gets <%d> rels.' % (query, len(ans)))
    except:
        print('Fail')
        return query
    return ans


if __name__ == "__main__":
    # baseDir = 'D:/Lab/HIN_PGCN'
    baseDir = '/home/LAB/penghao/croxx/HIN_PGCN'

    api_key = open(os.path.join(baseDir, 'files',
                                'google_knowledge_graph_api.key')).read()
    executor = ThreadPoolExecutor(max_workers=10)
    ens = pickle.load(
        open(os.path.join(baseDir, 'output', '_entities.pkl'), 'rb'))
    tasks = [executor.submit(lookup, args=(k, api_key)) for k, v in ens.keys()]
    rels = [task.result() for task in as_completed(tasks)]
    t = 0
    while True:
        t += 1
        cs = []
        print('Checking... ...')
        ok = 0
        for i,rel in enumerate(rels):
            if isinstance(rel,str):
                ok += 1
                cs.append(rel)
                rels[i] = lookup((rel,api_key))
        print('<%s> remains None, restarting...' % ok)
        pickle.dump(cs, open(os.path.join(baseDir, 'log', 'cs%03d.pkl' % t), 'wb'))
        if ok==0:
            break

    pickle.dump(ens, open(os.path.join(baseDir, 'output', '_rels.pkl'), 'wb'))
