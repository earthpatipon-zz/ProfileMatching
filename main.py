# -*- coding: utf-8 -*-

import pandas as pd
import collections
import math
from textblob import TextBlob as tb


# import data
data = pd.read_csv('thammasat.csv')

# Storage
dic = collections.defaultdict(dict)     # ['author name'] : { ['Author']: name, ['Address']: address, .... }
relatedList = []    # list of people related to keywords

# extract information from data
docList = data['Title']
abstractList = data['Abstract']
citedList = data['Cited by']
authorList = data['Authors with affiliations'].str.split(';')       # yield list ['name., address'] , ['name., address'], .....
authorKeywordList = data['Author Keywords'].str.split(';')          # yield list ['key1', 'key2', 'key3', ...., 'keyN']
indexKeywordList = data['Index Keywords'].str.split(';')            # yield list ['key1', 'key2', 'key3', ...., 'keyN']


for i in range(len(data)):
    keyword = authorKeywordList[i] if not(authorKeywordList[i]) else ''
    document = docList[i]

    for j in range(len(authorList[i])):
        authorAffiliation = authorList[i][j].split('.,')   # yield list ['name', 'address'] which index is [0,1]
        author = authorAffiliation[0]
        affiliation = authorAffiliation[1] if len(authorAffiliation) > 1 else ''

        if author not in dic:
            dic[author] = {'Author': author, 'Affiliation': affiliation, 'Document': document, 'Keyword': keyword}
            # print dic[author]

        else:
            add = dic[author]['Affiliation']
            doc = dic[author]['Document']
            key = dic[author]['Keyword']

            dic[author]['Document'] = doc + document
            if add == '':
                dic[author]['Address'] = add + affiliation
            if key == '':
                dic[author]['Keyword'] = keyword
            else:
                dic[author]['Keyword'] = key + keyword

for i in dic:
    print i[1]

# # take input
# query = raw_input("Keywords to find list of people related to: ")
# query = query.split(',')
#
# for k, v in dic.items():
#     for x in query:
#         if x in v['Keyword']:
#             relatedList.append({k:v})
#             continue;
#
# print relatedList
# for i in relatedList:
#     # print i.values()
#     for k in i:
#         print i[k]['Keyword']


# # td-idf (term frequency and inverse document frequency)
# def tf(word, blob):
#     return blob.words.count(word) / len(blob.words)
#
# def n_containing(word, bloblist):
#     return sum(1 for blob in bloblist if word in blob.words)
#
# def idf(word, bloblist):
#     return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))
#
# def tfidf(word, blob, bloblist):
#     return tf(word, blob) * idf(word, bloblist)
#
#
# for i, blob in enumerate(abstractList):
#     print("Top words in document {}".format(i + 1))
#     scores = {word: tfidf(word, blob, abstractList) for word in blob.words}
#     sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
#     for word, score in sorted_words[:3]:
#         print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
