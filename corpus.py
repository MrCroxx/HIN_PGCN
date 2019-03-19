import os.path
import pickle
import re
from xml.etree import ElementTree

import nltk


def pickTextAndTopicFromXml(path: str):
    tree = ElementTree.parse(path)
    newsItem = tree.getroot()
    text = ''
    topiccodes = []

    titleItem = newsItem.find('title')
    headlineItem = newsItem.find('headline')
    if titleItem is not None:
        if titleItem.text is not None:
            text += titleItem.text + '\n'
    if headlineItem is not None:
        if headlineItem.text is not None:
            text += headlineItem.text + '\n'
    textitem = newsItem.find('text')
    for item in textitem:
        text += item.text + '\n'

    codesItem = newsItem.iter('codes')
    topiccodesItem = None
    
    if codesItem is None:
        return None,None
    for item in codesItem:
        if item.attrib['class'] == 'bip:topics:1.0':
            topiccodesItem = item
            break
    if topiccodesItem is None:
        return None,None
    for codeItem in topiccodesItem:
        topiccodes.append(codeItem.attrib['code'])
    return text, topiccodes


def loadStops(path: str):
    stops = set()
    with open(path, 'r', encoding='utf8') as f:
        rows = f.readlines()
        for row in rows:
            stops.add(row[:-1])
    return stops


def containsAlphaOrNumber(s: str, reprog):
    return reprog.search(s) is not None


def removeStops(text: str, stops: set):
    reprog = re.compile(r'[a-z]')
    text_lower = text.lower()
    text_nstop = ''
    sents = nltk.sent_tokenize(text_lower)
    for sent in sents:
        words = nltk.word_tokenize(sent)
        for word in words:
            if containsAlphaOrNumber(word, reprog) and word not in stops:
                text_nstop += word + ' '
    return text_nstop


if __name__ == "__main__":
    # pickTextAndTopicFromXml(os.path.join('C:/Users/croxx/Desktop/rcv1', 'data', '382993newsML.xml'))
    # '''
    baseDir = 'C:/Users/croxx/Desktop/rcv1'
    stops = loadStops(os.path.join(baseDir, 'files/english.stop.txt'))
    files = os.listdir(os.path.join(baseDir, 'data'))

    docs = []
    codes = []
    texts = []
    cnt = 0
    for file in files:
        if file[-4:] != '.xml':
            continue
        
        text, codes_list = pickTextAndTopicFromXml(
            os.path.join(baseDir, 'data', file))
        if text is None:
            continue
        texts.append(text)

        
        text_nstop = removeStops(text, stops)
        code = ''
        for c in codes_list:
            code += c + ' '
        docs.append(text_nstop)
        codes.append(code)
        
        cnt += 1
        print('Processing %s xml <%s> ...' % (cnt,file))
    # Save to pkl
    pickle.dump(docs,open(os.path.join(baseDir,'output','docs.pkl'),'wb'))
    pickle.dump(codes,open(os.path.join(baseDir,'output','codes.pkl'),'wb'))  
    pickle.dump(texts,open(os.path.join(baseDir,'output','texts.pkl'),'wb'))
    # '''
