import json
import math
from collections import defaultdict

query = input("Please enter user input: ")
with open('index.json') as json_file:
    indexDict = json.load(json_file)
with open('bookkeeping.json') as json_file:
    bookkeepingDict = json.load(json_file)
links = indexDict[query]
linksList = list()
numberLinks = len(links)
for i in range(0,20):
    docId = (list(links[i].values())[0])
    linksList.append(bookkeepingDict[docId])

print(linksList, numberLinks)



# calculate the score of a document given the query word
def queryScore(document, querydict, querylength):

    index = json.load(open("indexWithNormalizedWeights.json"))
    docFreqindex = json.load(open("docFreq.json"))
    
    res = 0
    # get the query score for every word in the query
    for word in querydict:
        # iterate through all words and find the tokens that match the query word
        for token in index:
            if token == word:
                for doc in index[token]:
                    if doc == document:
                        prenormalized = ( 1 + math.log10(querydict[word]) ) * docFreqindex[word]
                        res += (prenormalized)/querylength * doc['weight']

                    break      
                break   # saves time? (because there's no need to iterate through rest of tokens if we already found)

    return res



def main():
    query = "best car insurance"

    # this keeps track of how many times each word appears in the query
    querydict = defaultdict(int)
    for word in query.lower.split():
        querydict[word] += 1

    # quickly compute the query length once, to get the normalization denominator to pass in function
    sum = 0
    docFreqindex = json.load(open("docFreq.json"))
    for word in querydict:
        for token in docFreqindex:
            if token == word:
                sum +=  ( ( 1 + math.log10(querydict[word]) ) * docFreqindex[word] )**2
    querylength = math.sqrt(sum)
    
    DocScores = {}  # dict to track document's query scores
    # for every document, calculate the query score
    
    for doc in document_list:
        DocScores[doc] = queryScore(doc, querydict, querylength)



    # now rank the documents best to last (the search results)
    return sorted(DocScores)[0]