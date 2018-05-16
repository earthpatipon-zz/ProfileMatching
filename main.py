# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import collections


# import data
data = pd.read_csv('dataset_100.csv')

# Storage
dic = collections.defaultdict(dict)         # ['author name'] : index of dicList
dicList = []        # list of dictionary
relatedList = []    # list of people related to keywords

# extract information from data
authorList = data['Authors with affiliations'].str.split(';')   # yield ['name., address'] , ['name., address'], .....
keywordList = data['Index Keywords'].str.split(';')             # yield ['key1', 'key2', 'key3', ...., 'keyN']
docList = data['Title']



#เคสชื่อซ้ำ ต้องเอา keyword มาใสดเพิ่ม doclist ด้วย

for i in range(len(data)):
    keyword = keywordList[i]
    document = docList[i]

    for j in range(len(authorList[i])):
        naList = authorList[i][j].split('.,')   # yield ['name', 'address'] which is <0,1>
        author = naList[0]
        address = naList[1] if len(naList) > 1 else ''

        if author not in dic:

            dic[author]= {'Author': author, 'Address': address, 'Keyword': keyword, 'Document': document}

            #dic[naList[0]] = i
           # dicList.append({'Author': author, 'Address': address, 'Keyword': keyword, 'Document': document})
        # else:
        #     add = dicList[i]['Address']
        #     key = dicList[i]['Keyword']
        #     doc = dicList[i]['Document']
        #
        #     dicList[i]['Address'] = add + address
        #     dicList[i]['Keyword'] = key + keyword
        #     dicList[i]['Document'] = doc + document

# # check
# for d in dicList:
#     print d

# take input
#query = raw_input("Keywords to find list of people related to: ")


print dic["Chumnumwat, S"]

print dic["Chumnumwat, S"]["Author"]
print dic["Chumnumwat, S"]["Keyword"]
print dic["Chumnumwat, S"]["Address"]
print dic["Chumnumwat, S"]["Document"]



# find keywords of each person
# def search(values, searchFor):
#     for k in values:
#         for v in values[k]:
#             if searchFor in v:
#                 return k
#     return None
#
#
#
# print relatedList










##### misc. #####

# to show all columns in dataframe
#print data.dtypes
# to show type of var
#print type(obc)