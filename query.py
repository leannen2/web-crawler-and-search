import json
import math
from collections import defaultdict

# query = input("Please enter user input: ")
# with open('index.json') as json_file:
#     indexDict = json.load(json_file)
# with open('bookkeeping.json') as json_file:
#     bookkeepingDict = json.load(json_file)
# links = indexDict[query]
# linksList = list()
# numberLinks = len(links)
# for i in range(0,20):
#     docId = (list(links[i].values())[0])
#     linksList.append(bookkeepingDict[docId])

# print(linksList, numberLinks)



# calculate the score of a document given the query word
def queryScore(query):

    # this keeps track of how many times each word appears in the query
    queryCount = defaultdict(int)
    wordlst = query.lower().split()
    for word in wordlst:
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
    


    DOCSCORES = defaultdict(int)

    index = json.load(open("indexWithNormalizedWeights.json"))
    
    # get the query score for every word in the query
    for word in queryCount:
        # iterate through all words and find the tokens that match the query word

        # what if the word is not in the index?

        for doc in index[word]:
            htmlweight = 0
            if doc["header"] != 0:
                htmlweight = 0.5 + math.log10(doc["header"])
                
            DOCSCORES[doc["docId"]] += (queryWeight[word])/querylength * doc["weight"] + htmlweight


    # return the top 20 results
    sortedScores = sorted(DOCSCORES.items(), key=lambda x:x[1], reverse=True)
    results = []
    for i in range(0,20):
        results.append(sortedScores[i])

    print(results)
    return results



def main():
    query = "Irvine"

    queryScore(query)



main()