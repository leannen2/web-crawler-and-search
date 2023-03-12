import json
import math
from collections import defaultdict
from nltk.stem import WordNetLemmatizer

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

def tokenize(text):
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
    token_count = {}
    for token in tokens:
        if token not in token_count:
            token_count[token] = 1
        else:
            token_count[token] += 1

    return token_count

def lemmatize_tokens(tokens):
    lemmatizer = WordNetLemmatizer()
    for index in range(len(tokens)):
        for l in ['n','v', 'a', 'r', 's']:
            lemma = lemmatizer.lemmatize(tokens[index], pos=l)
            if lemma != tokens[index]:
                tokens[index] = lemma
                break

# calculate the score of a document given the query word
def queryScore(query):
    queryCount = tokenize(query)


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
    query = "artificial intelligence"

    queryScore(query)



main()