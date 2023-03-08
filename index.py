import nltk #tokenizer
from nltk.tokenize.repp import ReppTokenizer # tokenizer
from nltk.stem import WordNetLemmatizer # lemmatization
from bs4 import BeautifulSoup 
import json
import psutil


def start_indexing():
    path_root = 'WEBPAGES_RAW/'
    index = {}
    for i in range(74):
        for j in range(500):
            print('RAM memory percent used:', psutil.virtual_memory()[2])
            path = f'{path_root}{i}/{j}'
            print(path)
            pageReader = open(path, encoding='utf-8')
            content = pageReader.read()
            soup = BeautifulSoup(content, features="lxml")
            text = soup.get_text()
            text = text.replace('\n',' ')
            tokens_dict = tokenize(text, f'{i}/{j}')
            tag_weight(tokens_dict, soup, f'{i}/{j}')
            add_tokens_to_index(tokens_dict, index)
    for j in range(497):
        print('RAM memory percent used:', psutil.virtual_memory()[2])
        path = f'{path_root}{74}/{j}'
        print(path)
        pageReader = open(path, encoding='utf-8')
        content = pageReader.read()
        soup = BeautifulSoup(content, features="lxml")
        text = soup.get_text()
        text = text.replace('\n',' ')
        tokens_dict = tokenize(text, f'{74}/{j}')
        tag_weight(tokens_dict, soup, f'{74}/{j}')
        add_tokens_to_index(tokens_dict, index)
    with open('index.json', 'w') as f:
        json.dump(index, f)


def tag_weight(index, soup, docId):
    # index = json.load(open("indexWithTfidf.json"))
    title = soup.find('title')
    if title:
        increment_tag_count(index, 'title', title.get_text(), docId)
    bold = soup.find('b')
    if bold:
        increment_tag_count(index, 'bold', bold.get_text(), docId)
    for headerNum in range(1,7):
        headerTag = f'h{headerNum}'
        header = soup.find(headerTag)
        if header:
            increment_tag_count(index, 'header', header.get_text(), docId)

def increment_tag_count(index, key, text, docId):
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
        if token not in index:
            print(f'{token} added to index')
            index[token] = {'docId':docId, 'count': 1}
        if key not in index[token]:
            index[token][key] = 1
        else:
            index[token][key] += 1

def tokenize(text, docId):
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
            token_count[token] = {'docId':docId, 'count': 1}
        else:
            token_count[token]['count'] += 1

    return token_count

def lemmatize_tokens(tokens):
    lemmatizer = WordNetLemmatizer()
    for index in range(len(tokens)):
        for l in ['n','v', 'a', 'r', 's']:
            lemma = lemmatizer.lemmatize(tokens[index], pos=l)
            if lemma != tokens[index]:
                tokens[index] = lemma
                break

def add_tokens_to_index(token_dict, index):
    for token in token_dict:
        if token in index:
            index[token].append(token_dict[token])
        else:
            index[token] = [token_dict[token]]
    
    

def test():
    # pageReader = open('WEBPAGES_RAW/0/2')
    # content = pageReader.read()
    # soup = BeautifulSoup(content, features="lxml")
    # text = soup.get_text()
    # text = text.replace('\n',' ')
    #print(text)

    #tokens = tokenizer.tokenize(text)
    # tokens_dict = tokenize(text, '0/2')
    #print(tokens_dict)
    # add_tokens_to_disk(tokens_dict)
    # json.dump(tokens_dict, open('other.json', 'w'))
    # lemmatizer = WordNetLemmatizer()
    # tokens = ['vertices', 'running', 'flower', 'objectively', 'quickly']
    # lemmatize_tokens(tokens)
    # print(tokens)
    path = 'WEBPAGES_RAW/26/325'
    pageReader = open(path, encoding='utf-8')
    content = pageReader.read()
    soup = BeautifulSoup(content, features="lxml")
    text = soup.get_text()
    text = text.replace('\n',' ')
    tokens = tokenize(text, '26/325')
    json.dump(tokens,open('test.json','w'))
    print(text)
    print(tokens)

if __name__ == "__main__":
    # import nltk
    # import ssl

    # try:
    #     _create_unverified_https_context = ssl._create_unverified_context
    # except AttributeError:
    #     pass
    # else:
    #     ssl._create_default_https_context = _create_unverified_https_context

    # nltk.download('wordnet')

    #test()

    start_indexing()


