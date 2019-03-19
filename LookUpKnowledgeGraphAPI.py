import json
import os
import os.path
import pickle
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests


def lookup(args):
    query, api_key = args
    # print('Looking up <%s>...' % (query,))
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    params = {
        'query': query,
        'limit': 10,
        'indent': True,
        'key': api_key,
    }
    proxies = {
        "http": "socks5://10.111.2.130:1080",
        'https': 'socks5//10.111.2.130:1080'
    }
    res = requests.get(service_url, params=params, proxies=proxies)
    j = json.loads(res.text)
    res = []
    for element in j['itemListElement']:
        if 'result' in element:
            if 'name' in element['result']:
                res.append(element['result']['name'])
    print('Lookup <%s> gets <%d> rels.' % (query, len(res)))
    return res


if __name__ == "__main__":
    # baseDir = 'D:/Lab/HIN_PGCN'
    baseDir = '/home/LAB/penghao/croxx/HIN_PGCN'
    api_key = open(os.path.join(baseDir, 'files',
                                'google_knowledge_graph_api.key')).read()
    executor = ThreadPoolExecutor(max_workers=1000)
    ens = pickle.load(
        open(os.path.join(baseDir, 'output', '_entities.pkl'), 'rb'))
    tasks = [executor.submit(lookup, args=(k, api_key)) for k, v in ens.keys()]
    rels = [task.result() for task in as_completed(tasks)]
    pickle.dump(ens, open(os.path.join(baseDir, 'output', '_rels.pkl'), 'wb'))
