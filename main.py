# -*- coding: utf-8 -*-

import collections
import math
import nltk
import pandas as pd
import numpy as np
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# import data
data = pd.read_csv('Thammasat.csv')

stop_words = set(stopwords.words('english'))
stop_words.update([',', '.', ':', '(', ')', '%'])

# Storage
dicAuthor = collections.defaultdict(dict)     # ['author name'] : { ['Author']: name, ['Affiliation']: affiliation, .... }
dicDocument = collections.defaultdict(dict)
relatedList = []    # list of people related to keywords

# extract information from data
docList = data['Title']
abstractList = data['Abstract']
citedList = data['Cited by']
authorList = data['Authors with affiliations'].str.split('; ')       # yield list ['name., address'] , ['name., address'], .....
#authorKeywordList = data['Author Keywords'].str.split('; ')          # yield list ['key1', 'key2', 'key3', ...., 'keyN']
#indexKeywordList = data['Index Keywords'].str.split('; ')            # yield list ['key1', 'key2', 'key3', ...., 'keyN']


for i in range(len(data)):
    document = docList[i]
    abstract_tokens = word_tokenize(abstractList[i])
    abstract = [w.lower() for w in abstract_tokens if w not in stop_words]
    #authorKeyword = authorKeywordList[i] if authorKeywordList[i] is not np.nan else []
    #authorKeyword = [w.lower() for w in authorKeyword]
    #indexKeyword = indexKeywordList[i] if indexKeywordList[i] is not np.nan else []
    #indexKeyword = [w.lower() for w in indexKeyword]

    for j in range(len(authorList[i])):
        authorAffiliation = authorList[i][j].split('.,')   # yield list ['name', 'address'] which index is [0,1]
        author = authorAffiliation[0]
        affiliation = authorAffiliation[1] if len(authorAffiliation) > 1 else []

        if author not in dicAuthor:
            document = [document]
            #authorKeyword = authorKeyword
            #indexKeyword = indexKeyword
            dicAuthor[author] = {'Author': author, 'Affiliation': affiliation, 'Document': document, 'Abstract': abstract}
                           #'AuthorKeyword': authorKeyword, 'IndexKeyword': indexKeyword}

        else:
            if not dicAuthor[author]['Affiliation']:
                dicAuthor[author]['Affiliation'] = affiliation
            dicAuthor[author]['Document'].append(document)
            if abstract:
                dicAuthor[author]['Abstract'].append(abstract)
            # if authorKeyword:
            #     dicAuthor[author]['AuthorKeyword'].append(authorKeyword)
            # if indexKeyword:
            #     dicAuthor[author]['IndexKeyword'].append(indexKeyword)

# #take input
# query = input("Keywords to find list of people related to: ")
# query = query.split(',')
# query = [s.lower() for s in query]
#
# for k, v in dicAuthor.items():
#     for x in query:
#         if x in v['Abstract']:
#             relatedList.append({k: v})
#             continue

# #check part
# print(len(relatedList))
# for i in relatedList:
#     for key in i:
#         print(key)
#         #print(i[key]['Abstract'])


# td-idf (term frequency and inverse document frequency)
def tf(word, blob):
    return blob.words.count(word) / len(blob.words)


def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)


def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))


def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)


blobList = []
for i in abstractList:
    blobList.append(TextBlob(i))

for i, blob in enumerate(blobList):
    print("Top words in document {}".format(i + 1))
    scores = {word: tfidf(word, blob, blobList) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:3]:
        print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))