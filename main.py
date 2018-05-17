# -*- coding: utf-8 -*-

import pandas as pd
import collections


# import data
data = pd.read_csv('dataset_100.csv')

# Storage
dic = collections.defaultdict(dict)     # ['author name'] : { ['Author']: name, ['Address']: address, .... }
relatedList = []    # list of people related to keywords

# extract information from data
authorList = data['Authors with affiliations'].str.split(';')   # yield list ['name., address'] , ['name., address'], .....
keywordList = data['Index Keywords'].str.split(';')             # yield list ['key1', 'key2', 'key3', ...., 'keyN']
docList = data['Title']


for i in range(len(data)):
    keyword = keywordList[i]
    document = docList[i]

    for j in range(len(authorList[i])):
        naList = authorList[i][j].split('.,')   # yield list ['name', 'address'] which index is [0,1]
        author = naList[0]
        address = naList[1] if len(naList) > 1 else ''

        if author not in dic:
            dic[author] = {'Author': author, 'Address': address, 'Keyword': keyword, 'Document': document}
            #print dic[author]

        else:
            add = dic[author]['Address']
            key = dic[author]['Keyword']
            doc = dic[author]['Document']

            if add == '':
                dic[author]['Address'] = add + address

            dic[author]['Keyword'] = key + keyword
            dic[author]['Document'] = doc + document
            # print "####################################"
            # print dic[author]
            # print type(dic['Address'])
            # print type(dic['Keyword'])
            # print type(dic['Document'])

# take input
query = raw_input("Keywords to find list of people related to: ")
query = query.split(',')

for k, v in dic.items():
    for x in query:
        if x in v['Keyword']:
            relatedList.append({k:v})
            continue;


for i in relatedList:
    #print i.values()
    for k in i:
        print i[k]['Keyword']