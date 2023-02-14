import nltk #tokenizer
from nltk.tokenize.repp import ReppTokenizer # tokenizer
from nltk.stem import WordNetLemmatizer # lemmatization
from bs4 import BeautifulSoup 
#nltk.download('wordnet') # needed to run lemmatize

def start_indexing():
    a_f = open('a-f.json', 'w')
    g_p = open('g-p.json', 'w')
    q_z = open('q-z.json', 'w')
    

def index_page(pageId, tokens):
    pass

def tokenize(text):
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


    return tokens

def lemmatize_tokens(tokens):
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    #print('testing lemmatize', lemmatizer.lemmatize("ponies"))
    return tokens
# tokenizer = ReppTokenizer('/home/alvas/repp/') 

def test():
    pageReader = open('WEBPAGES_RAW/0/2')
    content = pageReader.read()
    soup = BeautifulSoup(content, features="lxml")
    text = soup.get_text()
    text = text.replace('\n',' ')
    #print(text)

    #tokens = tokenizer.tokenize(text)
    tokens = tokenize(text)
    print(tokens)

if __name__ == "__main__":
    test()

