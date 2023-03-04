import json
import math

def calc_weight():
    index = json.load(open("index.json"))
    for token in index:
        numOfDocs = len(index[token])
        docFrequency = math.log10(37498/numOfDocs) # log(N/df)
        for doc in index[token]:
            termFrequency = 1 + math.log10(doc['count']) # 1 + log(tf)
            doc['tfidf'] = termFrequency * docFrequency
    json.dump(index, open('newIndex.json', 'w'))
    

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

if __name__ == "__main__":
    calc_weight()