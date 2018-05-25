# -*- coding: utf-8 -*-

import collections
import nltk

import pandas as pd
import numpy as np
import textblob as tb

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# import data
data = pd.read_csv('thammasat.csv')
stop_words = set(stopwords.words('english'))

# Storage
dic = collections.defaultdict(dict)     # ['author name'] : { ['Author']: name, ['Address']: address, .... }
relatedList = []    # list of people related to keywords

# extract information from data
docList = data['Title']
abstractList = data['Abstract']
citedList = data['Cited by']
authorList = data['Authors with affiliations'].str.split('; ')       # yield list ['name., address'] , ['name., address'], .....
authorKeywordList = data['Author Keywords'].str.split('; ')          # yield list ['key1', 'key2', 'key3', ...., 'keyN']
indexKeywordList = data['Index Keywords'].str.split('; ')            # yield list ['key1', 'key2', 'key3', ...., 'keyN']

for i in range(len(data)):
    document = docList[i]
    abstract_tokens = word_tokenize(abstractList[i])
    abstract = [w for w in abstract_tokens if not w in stop_words]
    authorKeyword = authorKeywordList[i] if authorKeywordList[i] is not np.nan else []
    indexKeyword = indexKeywordList[i] if indexKeywordList[i] is not np.nan else []

    for j in range(len(authorList[i])):
        authorAffiliation = authorList[i][j].split('.,')   # yield list ['name', 'address'] which index is [0,1]
        author = authorAffiliation[0]
        affiliation = authorAffiliation[1] if len(authorAffiliation) > 1 else []

        if author not in dic:
            document = [document]
            authorKeyword = authorKeyword
            indexKeyword = indexKeyword
            dic[author] = {'Author': author, 'Affiliation': affiliation, 'Document': document,
                           'Abstract': abstract, 'AuthorKeyword': authorKeyword, 'IndexKeyword': indexKeyword}

        else:
            if not dic[author]['Affiliation']:
                dic[author]['Affiliation'] = affiliation
            dic[author]['Document'].append(document)
            if abstract:
                dic[author]['Abstract'].append(abstract)
            if authorKeyword:
                dic[author]['AuthorKeyword'].append(authorKeyword)
            if indexKeyword:
                dic[author]['IndexKeyword'].append(indexKeyword)


#take input
query = input("Keywords to find list of people related to: ")
query = query.split(',')

for k, v in dic.items():
    for x in query:
        if x in v['IndexKeyword']:
            relatedList.append({k:v})
            continue;


for i in relatedList:
    for key in i:
        print(key)
        print(i[key]['Abstract'])
    # for k in i:
    #     print(i[k]['Author'])


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
# document1 = tb("""Python is a 2000 made-for-TV horror movie directed by Richard
# Clabaugh. The film features several cult favorite actors, including William
# Zabka of The Karate Kid fame, Wil Wheaton, Casper Van Dien, Jenny McCarthy,
# Keith Coogan, Robert Englund (best known for his role as Freddy Krueger in the
# A Nightmare on Elm Street series of films), Dana Barron, David Bowe, and Sean
# Whalen. The film concerns a genetically engineered snake, a python, that
# escapes and unleashes itself on a small town. It includes the classic final
# girl scenario evident in films like Friday the 13th. It was filmed in Los Angeles,
#  California and Malibu, California. Python was followed by two sequels: Python
#  II (2002) and Boa vs. Python (2004), both also made-for-TV films.""")
#
# document2 = tb("""Python, from the Greek word (πύθων/πύθωνας), is a genus of
# nonvenomous pythons[2] found in Africa and Asia. Currently, 7 species are
# recognised.[2] A member of this genus, P. reticulatus, is among the longest
# snakes known.""")
#
# document3 = tb("""The Colt Python is a .357 Magnum caliber revolver formerly
# manufactured by Colt's Manufacturing Company of Hartford, Connecticut.
# It is sometimes referred to as a "Combat Magnum".[1] It was first introduced
# in 1955, the same year as Smith &amp; Wesson's M29 .44 Magnum. The now discontinued
# Colt Python targeted the premium revolver market segment. Some firearm
# collectors and writers such as Jeff Cooper, Ian V. Hogg, Chuck Hawks, Leroy
# Thompson, Renee Smeets and Martin Dougherty have described the Python as the
# finest production revolver ever made.""")
#
# abstractList = [document1,document2,document3]
#
# for i, blob in enumerate(abstractList):
#     print("Top words in document {}".format(i + 1))
#     scores = {word: tfidf(word, blob, abstractList) for word in blob.words}
#     sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
#     for word, score in sorted_words[:3]:
#         print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
#         #         print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
#         if add == '':
#             dic[author]['Address'] = add + affiliation
#         if key == '':
#             dic[author]['Keyword'] = keyword
#         else:
#             dic[author]['Keyword'] = key + keyword
#
# for i in dic:
#     print(i[1])