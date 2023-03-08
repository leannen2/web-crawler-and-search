import json
import math
from bs4 import BeautifulSoup 
from lxml import html
from index import lemmatize_tokens

def calc_weight(indexFile):
    index = json.load(open(indexFile))
    docLengthIndex = {}
    docFreqDict = {}
    for token in index:
        numOfDocs = len(index[token])
        docFrequency = math.log10(37498/numOfDocs) # log(N/df)
        docFreqDict[token] = docFrequency
        for doc in index[token]:
            termFrequency = 1 + math.log10(doc['count']) # 1 + log(tf)
            docLengthIndex[doc['docId']] = docLengthIndex.get(doc['docId'], 0) + (termFrequency**2)
            doc['weight'] = termFrequency
            if 'title' not in doc:
                doc['title'] = 0
            if 'header' not in doc:
                doc['header'] = 0
            if 'bold' not in doc: 
                doc['bold'] = 0
    
    for token in index:
        for doc in index[token]:
            doc['weight'] = doc['weight'] / (docLengthIndex[doc['docId']] ** 0.5)

    json.dump(index, open('newIndex.json', 'w'))
    json.dump(docFreqDict, open('docFreq.json', 'w'))
    json.dump(docLengthIndex, open('docLength.json', 'w'))
    

def test_calc_weight():
    index = json.load(open("index.json"))
    for token in index:
        numOfDocs = len(index[token])
        docFrequency = math.log10(37498/numOfDocs)
        for doc in index[token]:
            termFrequency = 1 + math.log10(doc['count'])
            doc['tfidf'] = termFrequency * docFrequency
        subIndex = index[token]
        print(token)
        json.dump(subIndex, open('newIndex.json', 'w'))
        break

def tag_weight():
    index = json.load(open("indexWithTfidf.json"))
    path_root = 'WEBPAGES_RAW/'
    index = {}
    for i in range(74):
        for j in range(500):
            path = f'{path_root}{i}/{j}'
            print(path)
            pageReader = open(path, encoding='utf-8')
            content = pageReader.read()
            soup = BeautifulSoup(content, features="lxml")
            title = soup.find('title')
            if title:
                increment_tag_count(index, 'title', f'{i}/{j}', title.get_text())
            bold = soup.find('b')
            if bold:
                increment_tag_count(index, 'bold', f'{i}/{j}', bold.get_text())
            for headerNum in range(1,7):
                headerTag = f'h{headerNum}'
                header = soup.find(headerTag)
                if header:
                    increment_tag_count(index, 'header', f'{i}/{j}', header.get_text())
            
    for j in range(497):
        path = f'{path_root}{74}/{j}'
        print(path)
        pageReader = open(path, encoding='utf-8')
        content = pageReader.read()
        soup = BeautifulSoup(content, features="lxml")
        title = soup.find('title')
        if title:
            increment_tag_count(index, 'title', f'{74}/{j}', title.get_text())
        bold = soup.find('b')
        if bold:
            increment_tag_count(index, 'bold', f'{74}/{j}', bold.get_text())
        for headerNum in range(1,7):
            headerTag = f'h{headerNum}'
            header = soup.find(headerTag)
            if header:
                increment_tag_count(index, 'header', f'{74}/{j}', header.get_text())

    json.dump(index,open('indexWithTfidfAndTagWeights.json', 'w'))

def test_html_weight():
    index = {}
    path = 'WEBPAGES_RAW/3/7'
    pageReader = open(path, encoding='utf-8')
    content = pageReader.read()
    soup = BeautifulSoup(content, features="lxml")
    title = soup.find('title')
    if title:
        increment_tag_count(index, 'title', path, title.get_text())
    bold = soup.find('b')
    if bold:
        increment_tag_count(index, 'bold', path, bold.get_text())
    header = soup.find('h3')
    for headerNum in range(1,7):
        headerTag = f'h{headerNum}'
        header = soup.find(headerTag)
        if header:
            increment_tag_count(index, 'header', path, header.get_text())
    print(index)

def increment_tag_count(index, key, docId, text):
    stopWords = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours\tourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves']
    tokens = ''
    for a in text:
        if a.isalnum() ==  False or a.isascii() == False:
            tokens+= ' '
        else:
            tokens+=a
    tokens = tokens.lower().split()
    lemmatize_tokens(tokens)
    tokens = list(filter(lambda x: x not in stopWords and len(x) > 2, tokens))
    for token in tokens:
        # if token not in index:
        #     index[token] = {'docId':docId, key: 1}
        if key not in index[token]:
            index[token][key] = 1
        else:
            index[token][key] += 1

def sqRtDocLength(fileName):
    docLength = json.load(open(fileName))
    for doc in docLength:
        docLength[doc] = docLength[doc] ** 0.5
    json.dump(docLength, open('docLength.json', 'w'))

if __name__ == "__main__":
    #test_html_weight()
    # tag_weight()
    # calc_weight('indexWithTagWeightAndTfidf.json')
    sqRtDocLength('docLength-no sq root.json')