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
def queryScore(query):

    # this keeps track of how many times each word appears in the query
    queryCount = defaultdict(int)
    for word in query.lower.split():
        queryCount[word] += 1


    # quickly compute the query weights
    # and query length once (normalization denominator)
    docFreqindex = json.load(open("docFreq.json"))
    queryWeight = {}
    sum = 0
    for word in queryCount:
        for token in docFreqindex:
            if token == word:
                weight = ( 1 + math.log10(queryCount[word]) ) * docFreqindex[word]
                queryWeight[word] = weight
                sum +=  weight**2
    querylength = math.sqrt(sum)
    


    DOCSCORES = {}

    index = json.load(open("indexWithNormalizedWeights.json"))
    
    # get the query score for every word in the query
    for word in queryCount:
        # iterate through all words and find the tokens that match the query word
            for doc in index[word]:    
                DOCSCORES[doc["docId"]] += (queryWeight[word])/querylength * doc["weight"]


    # return the top 20 results
    sortedScores = list( sorted(DOCSCORES.items(), key=lambda x:x[1]).keys() )
    results = []
    i = 0
    while i < 20:
        results.append(sortedScores[i])
        i += 1

    return results





def main():
    query = "best car insurance"

    queryScore(query)