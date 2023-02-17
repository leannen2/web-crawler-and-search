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