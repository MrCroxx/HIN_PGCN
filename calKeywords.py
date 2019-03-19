import os.path
import pickle
from concurrent.futures import ThreadPoolExecutor

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

def processRow(args):
    i,row,word,path = args
    path_row = os.path.join(path,'keys','row_%08d' % i)
    if os.path.exists(path_row):
        return None
    max_keys = 100
    key = sorted(zip(word,row),key=lambda x:x[1],reverse=True)

    newrow = [ w for w,r in key[:max_keys if max_keys>0 else len(key)] ]
    newrow += [ '' for i in range(max_keys-len(newrow)) ]
    
    pickle.dump(newrow,open(path_row,'wb'))
    print('Row %s dumped.' %i)

def generateKeywords(path:str):
    corpus = pickle.load(open(os.path.join(path,'docs.pkl'),'rb'))
    print('Finish reading pkl file.')
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus) # 词频矩阵
    print('Finish calculating frequency matrix.')
    word = vectorizer.get_feature_names() # 关键词
    print('Finish calculating keywords.')
    transformer = TfidfTransformer()
    TF_IDF = transformer.fit_transform(X)
    print('Finish calculating TF-IDF matrix.')

    executor = ThreadPoolExecutor(max_workers=1000)   
    
    for i in range(TF_IDF.shape[0]):
        row = TF_IDF[i,:].toarray()[0]
        print('Sorting row %s ...' % i)
        executor.submit(processRow,(i,row,word,path))
       
    executor.shutdown(wait=True)

def combineKeys(dirpath,outpath):
    print('Reading file list.')
    files = os.listdir(dirpath)
    files = sorted(files,reverse=False)
    keywords = []
    for file in files:
        print('Processing file %s' % file)
        path = os.path.join(dirpath,file)
        f = open(path,'rb')
        row = pickle.load(f)
        keywords.append(row)
    pickle.dump(keywords,open(outpath,'wb'))
    print('Finish combining Keywords.')



if __name__ == "__main__":
    # baseDir = 'C:/Users/croxx/Desktop/rcv1'
    baseDir = '/home/LAB/penghao/croxx/HIN'
    generateKeywords(os.path.join(baseDir,'output'))
    combineKeys(os.path.join(baseDir,'output','keys'),os.path.join(baseDir,'output','keys.pkl'))
