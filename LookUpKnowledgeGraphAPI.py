import json
import os
import os.path
import pickle
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

'''
def lookup(args):
    query, api_key = args
    if os.path.exists('/home/LAB/penghao/croxx/HIN_PGCN/output/rels/%s' % query):
        return None
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
    pickle.dump(ans,open('/home/LAB/penghao/croxx/HIN_PGCN/output/rels/%s' % query,'wb'))
    return ans
'''


def lookup(args):
    query, api_key = args
    query = query.replace('/','_')
    if os.path.exists('/home/LAB/penghao/croxx/HIN_PGCN/output/dbpedia/%s' % query):
        return None
    url = 'http://lookup.dbpedia.org/api/search/KeywordSearch'
    headers = {
        'Accept': 'application/json'
    }
    params = {
        'QueryString': query,
        'QueryClass': '',
        'MaxHits': 100
    }
    ans = []
    try:
        res = requests.get(url, headers=headers, params=params)
        if res.status_code != 200:
            print('Fail')
            return query
        j = json.loads(res.text)

        for r in j['results'][1:]:
            ans.append(r['label'])
        print('Lookup <%s> gets <%d> rels.' % (query, len(ans)))
    except:
        print('Fail')
        return query
    pickle.dump(
        ans, open('/home/LAB/penghao/croxx/HIN_PGCN/output/dbpedia/%s' % query, 'wb'))
    return ans


if __name__ == "__main__":
    # baseDir = 'D:/Lab/HIN_PGCN'
    baseDir = '/home/LAB/penghao/croxx/HIN_PGCN'

    api_key = open(os.path.join(baseDir, 'files',
                                'google_knowledge_graph_api.key')).read()
    executor = ThreadPoolExecutor(max_workers=100)
    ens = pickle.load(
        open(os.path.join(baseDir, 'output', '_entities.pkl'), 'rb'))

    # tasks = [executor.submit(lookup, args=(k, api_key)) for k, v in ens.keys()]
    # rels = [task.result() for task in as_completed(tasks)]

    for k, v in ens.keys():
        executor.submit(lookup, args=(k, api_key))
    executor.shutdown(wait=True)
