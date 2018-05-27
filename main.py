# -*- coding: utf-8 -*-

import collections
import math
import pandas as pd
import numpy as np
import operator
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from datetime import datetime

start_time = datetime.now()
stop_words = set(stopwords.words('english'))
stop_words.update([',', '.', ':', '(', ')', '%', 'a', 'in', 'to', 's', 'the', '©', '&', 'this', 'that'])

# import data
data = pd.read_csv('dataset.csv')

# Dict
dicAuthor = collections.defaultdict(dict)           # 'author name': {'Author': , 'Affiliation': , 'Document': }
dicAuthorTFIDF = collections.defaultdict(dict)      # 'author name': {'vector': [list of vectors], 'document': [list of documents]}
dicDocument = collections.defaultdict(dict)         # 'document name': {'Abstract': ,'Author': }
dicDocumentIndex = collections.defaultdict(dict)    # 'index number': document name
dicKeyword = collections.defaultdict(dict)          # 'keyword': {'Abstract', 'Author'}
dicRank = collections.defaultdict(dict)             # 'author name': cosine-sim score

# extract information from data
documentList = data['Title']
abstractList = data['Abstract']
authorList = data['Authors with affiliations'].str.split('; ')  # yield list ['name., address'] , ['name., address']
# authorKeywordList = data['Author Keywords'].str.split('; ')       # yield list ['key1', 'key2', 'key3', ...., 'keyN']
# indexKeywordList = data['Index Keywords'].str.split('; ')         # yield list ['key1', 'key2', 'key3', ...., 'keyN']

abstractReducedList = []    # list of cut stop word abstract

for i in range(len(data)):
    document = documentList[i]
    dicDocumentIndex[i] = document
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
query = input("Keywords to find list of people related to: ")
query = query.split(', ')
query = [s.lower() for s in query]
docSearchList = []       # list of document name which contain keywords in abstract
abstractSearchList = []  # list of abstract docs which contain keywords in abstract

for i, x in enumerate(abstractReducedList):
    for word in query:
        if word in x:
            docSearchList.append(dicDocumentIndex[i])
            abstractSearchList.append(x)
            continue

if(len(abstractSearchList)) == 0:
    print("No matching results")
    exit()

for word in query:
    dicKeyword[word] = {'Document': [], 'Author': []}

for k, v in dicDocument.items():
    for word in query:
        if word in v['Abstract']:
            dicKeyword[word]['Document'].append([k])
            temp = []
            for name in v['Author']:
                temp.append(name)
            dicKeyword[word]['Author'].append(temp)

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
for i in abstractSearchList:
    blobList.append(TextBlob(' '.join(i)))

for i, blob in enumerate(blobList):
    for word in query:
        score = {word: tfidf(word, blob, blobList) for word in query}
        scoreVector = [v for k, v in score.items()]

        for j, x in enumerate(dicKeyword[word]['Author']):
            for author in x:
                doc = docSearchList[i]
                if doc in dicKeyword[word]['Document'][j]:
                    if author not in dicAuthorTFIDF:
                        dicAuthorTFIDF[author] = {'Document': [docSearchList[i]], 'Vector': [scoreVector]}
                    else:
                        dicAuthorTFIDF[author]['Document'].append(docSearchList[i])
                        dicAuthorTFIDF[author]['Vector'].append(scoreVector)

# iterates to get mean value of vector
for k, v in dicAuthorTFIDF.items():
    mean = []
    temp = []
    n = 0
    for word in query:
        mean.append(0)      # mean = [0, 0, 0, ... ]
        temp.append(0)
    for i in v['Vector']:
        for j in i:
            temp = [x+y for x, y in zip(temp, i)]
            n = n + 1
    mean = [x+y for x, y in zip(mean,temp)]
    mean = np.array(mean, dtype=np.float)
    mean = mean/n
    dicAuthorTFIDF[k]['VectorMean'] = mean

vectorQuery = []
for word in query:
    vectorQuery.append(1)       # [1, 1, 1, ...]
vectorQuery = np.array(vectorQuery)

for k, v in dicAuthorTFIDF.items():
    vectorPerson = v['VectorMean']
    if (np.linalg.norm(vectorQuery) * np.linalg.norm(vectorPerson)) == 0.0:     # if vector is [0, 0, 0, ..] continue
        continue
    dicRank[k] = (cos_sim(vectorQuery, vectorPerson))

rank = dict(sorted(dicRank.items(), key=operator.itemgetter(1), reverse=True)[:5])
for k, v in rank.items():
    print(k + "   CosineSim score: " + str(v))
    print("Affiliation: " + dicAuthor[k]['Affiliation'])
    print()

end_time = datetime.now()
print()
print('Duration: {}'.format(end_time - start_time))