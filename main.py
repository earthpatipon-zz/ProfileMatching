# -*- coding: utf-8 -*-

import collections
import math
import pandas as pd
import numpy as np
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from datetime import datetime

# import data
start_time = datetime.now()

data = pd.read_csv('thammasat.csv')
stop_words = set(stopwords.words('english'))
stop_words.update([',', '.', ':', '(', ')', '%', 'a', 'in', 'to', 's', 'the', '©', '&', 'this', 'that'])

# Dict
dicAuthor = collections.defaultdict(dict)           # 'author name': {'Author': , 'Affiliation': , 'Document': }
dicDocument = collections.defaultdict(dict)         # 'document name': {'Abstract': ,'Author': }
dicKeyword = collections.defaultdict(dict)
dicAuthorTFIDF = collections.defaultdict(dict)  # 'author name': {'vector': [list of vectors], 'document': [list of documents]}


# extract information from data
documentList = data['Title']
abstractList = data['Abstract']
authorList = data['Authors with affiliations'].str.split('; ')  # yield list ['name., address'] , ['name., address']
# authorKeywordList = data['Author Keywords'].str.split('; ')       # yield list ['key1', 'key2', 'key3', ...., 'keyN']
# indexKeywordList = data['Index Keywords'].str.split('; ')         # yield list ['key1', 'key2', 'key3', ...., 'keyN']
abstractReducedList = []    # list of cut stop word abstract


for i in range(len(data)-1500):
    document = documentList[i]
    tokens = word_tokenize(abstractList[i])
    abstractKeyword = [w.lower() for w in tokens if w.lower() not in stop_words]
    abstractReducedList.append(abstractKeyword)
    # authorKeyword = authorKeywordList[i] if authorKeywordList[i] is not np.nan else []
    # authorKeyword = [w.lower() for w in authorKeyword]
    # indexKeyword = indexKeywordList[i] if indexKeywordList[i] is not np.nan else []
    # indexKeyword = [w.lower() for w in indexKeyword]

    for j in range(len(authorList[i])):
        authorAffiliation = authorList[i][j].split('.,')  # yield list ['name', 'address'] which index is [0,1]
        author = authorAffiliation[0]
        affiliation = authorAffiliation[1] if len(authorAffiliation) > 1 else []

        if author not in dicAuthor:
            doc = [document]
            # authorKeyword = authorKeyword
            # indexKeyword = indexKeyword
            dicAuthor[author] = {'Author': author, 'Affiliation': affiliation, 'Document': [document]}
            # , 'Abstract': abstractKeyword, 'AuthorKeyword': authorKeyword, 'IndexKeyword': indexKeyword}

        else:
            if not dicAuthor[author]['Affiliation']:
                dicAuthor[author]['Affiliation'] = affiliation
            dicAuthor[author]['Document'].append(document)
            # dicAuthor[author]['Abstract'].append(abstractKeyword)
            # if authorKeyword:
            #     dicAuthor[author]['AuthorKeyword'].append(authorKeyword)
            # if indexKeyword:
            #     dicAuthor[author]['IndexKeyword'].append(indexKeyword)

        if document not in dicDocument:
            dicDocument[document] = {'Abstract': abstractKeyword, 'Author': [author]}
        else:
            dicDocument[document]['Author'].append(author)


# take input
# query = input("Keywords to find list of people related to: ")
# query = ["relationship", "system", "temperature", "energies"]
query = ["mapping", "synthetic", "temperature", "energies"] # for thammasat - 1500
query = [s.lower() for s in query]
abstractSearchList = []  # list of abstract docs which contain keywords in abstract

for word in query:
    dicKeyword[word] = {'Document': [], 'Author': []}


for k, v in dicDocument.items():
    for word in query:
        if word in v['Abstract']:
            dicKeyword[word]['Document'].append(k)
            temp = []
            for name in v['Author']:
                temp.append(name)
            dicKeyword[word]['Author'].append(temp)

print(dicKeyword)

for i in abstractReducedList:
    for word in query:
        if word in i:
            abstractSearchList.append(i)
            continue


# td-idf (term frequency and inverse document frequency)
def tf(word, blob):
    return blob.words.count(word) / len(blob.words)


def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)


def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))


def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)


def cos_sim(a, b):
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)


blobList = []       # list of abstract documents
vectorList = []     # vector of keyword in query

for i in abstractSearchList:
    blobList.append(TextBlob(' '.join(i)))

for blob in blobList:
    for word in query:
        score = {word: tfidf(word, blob, blobList) for word in query}
        scoreVector = [v for k, v in score.items()]

        for i, x in enumerate(dicKeyword[word]['Author']):
            for author in x:
                if author not in dicAuthorTFIDF:
                    dicAuthorTFIDF[author] = {'Document': dicKeyword[word]['Document'][i], 'Vector': [scoreVector]}

        vectorList.append(scoreVector)


print(dicAuthorTFIDF)

for i in range(len(vectorList) - 1):

    VectorA = np.array(vectorList[i])

    VectorB = np.array(vectorList[len(vectorList) - 1])

    if ((np.linalg.norm(VectorA) * np.linalg.norm(VectorB)) == 0.0):
        continue

    print((cos_sim(VectorA, VectorB)))

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))

# VectorBVectorA = np.array(vectorList[4])
#
# VectorB = np.array(vectorList[len(vectorList)-1])
#
# print((cos_sim(VectorA,VectorB)))


# print (scoresList[i])


# print("\tWord: {}, TF-IDF: {}".format(word, round(scores[i], 5)))


# sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
# for word, score in sorted_words[:3]:
#    print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
