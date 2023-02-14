import nltk #tokenizer
from nltk.tokenize.repp import ReppTokenizer # tokenizer
from nltk.stem import WordNetLemmatizer # lemmatization
from bs4 import BeautifulSoup 
import json
import psutil


def start_indexing():
    path_root = 'WEBPAGES_RAW/'
    for i in range(1):
        for j in range(250):
            print('RAM memory percent used:', psutil.virtual_memory()[2])
            path = f'{path_root}{i}/{j}'
            print(path)
            pageReader = open(path)
            content = pageReader.read()
            soup = BeautifulSoup(content, features="lxml")
            text = soup.get_text()
            text = text.replace('\n',' ')
            tokens_dict = tokenize(text, f'{i}/{j}')
            add_tokens_to_disk(tokens_dict)

def index_page(pageId, tokens):
    pass

def tokenize(text, docId):
    stopWords = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours\tourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves']
    tokens = ''
    for a in text:
        if a.isalnum() ==  False:
            tokens+= ' '
        else:
            tokens+=a
    tokens = tokens.lower().split()
    tokens = lemmatize_tokens(tokens)
    tokens = list(filter(lambda x: x[0] not in stopWords and len(x) > 2, tokens))
    token_count = {}
    for token in tokens:
        if token not in token_count:
            token_count[token] = {'docId':docId, 'count': 1}
        else:
            token_count[token]['count'] += 1

    return token_count

def lemmatize_tokens(tokens):
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    #print('testing lemmatize', lemmatizer.lemmatize("ponies"))
    return tokens
# tokenizer = ReppTokenizer('/home/alvas/repp/') 

def add_tokens_to_disk(token_dict):
    # a_f = open('a-f.json', 'a+')
    # g_p = open('g-p.json', 'a+')
    # q_z = open('q-z.json', 'a+')
    # other = open('other.json', 'a+')
    a_dict = json.load(open('a-f.json'))
    g_dict = json.load(open('g-p.json'))
    q_dict = json.load(open('q-z.json'))
    other_dict = json.load(open('other.json'))
    for token in token_dict:
        if token[0] >= 'a' and token[0] <= 'f':
            if token in a_dict:
                a_dict[token].append(token_dict[token])
            else:
                a_dict[token] = [token_dict[token]]
        elif token[0] >= 'g' and token[0] <= 'p':
            if token in g_dict:
                g_dict[token].append(token_dict[token])
            else:
                g_dict[token] = [token_dict[token]]
        elif token[0] >= 'q' and token[0] <= 'z':
            if token in q_dict:
                q_dict[token].append(token_dict[token])
            else:
                q_dict[token] = [token_dict[token]]
        else:
            if token in other_dict:
                other_dict[token].append(token_dict[token])
            else:
                other_dict[token] = [token_dict[token]]

    json.dump(a_dict, open('a-f.json', 'w'))
    json.dump(g_dict, open('g-p.json', 'w'))
    json.dump(q_dict, open('q-z.json', 'w'))
    json.dump(other_dict, open('other.json', 'w'))

def test():
    pageReader = open('WEBPAGES_RAW/0/2')
    content = pageReader.read()
    soup = BeautifulSoup(content, features="lxml")
    text = soup.get_text()
    text = text.replace('\n',' ')
    #print(text)

    #tokens = tokenizer.tokenize(text)
    tokens_dict = tokenize(text, '0/2')
    #print(tokens_dict)
    add_tokens_to_disk(tokens_dict)
    json.dump(tokens_dict, open('other.json', 'w'))

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

