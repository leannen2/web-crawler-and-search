import json

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



# calculate the score of a document given the query
def queryScore(query, document):
    # we get the sum of the query/document weight
    res = 0
    for word in query:
        # obtain the weight of the word in the document
        index = json.load(open("index.json"))
        for token in index:
            if token == word:
                for doc in index[token]:
                    if doc == document:
                        res += doc['tfidf']
                break   # saves time? (because there's no need to iterate through rest of tokens if we already found)
            
    return res



# def main():
#     query = ""

#     DocScores = {}  # dict to track document's query scores
#     # for every document, calculate the query score
#     for doc in document_list:
#         DocScores[doc] = queryScore(query, doc)

#     # now rank the documents best to last (the search results)
#     return sorted(DocScores)