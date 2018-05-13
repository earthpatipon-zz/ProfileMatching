import pandas as pd
import numpy as np

# import data
data = pd.read_csv('dataset.csv')

# Storage
dic = {}        # ['author name'] : index of dicList
dicList = []    # list of dictionary

# extract information from data
authorList = data['Authors with affiliations'].str.split(';')   # yield ['name., address'] , ['name., address'], .....
keywordList = data['Index Keywords'].str.split(';')             # yield ['key1', 'key2', 'key3', ...., 'keyN']
docList = data['Title']

for i in range(len(data)):
    keyword = keywordList[i]
    document = docList[i]

    for j in range(len(authorList[i])):
        author = authorList[i][j].split('.,')   # yield ['name', 'address'] which is <0,1>
        address = author[1] if len(author) > 1 else ''

        if author[0] not in dic:
            dic[author[0]] = i
            dicList.append({'Author': author[0], 'Address': address, 'Keyword': keyword, 'Document': document})
        else:
            add = dicList[i]['Address']
            key = dicList[i]['Keyword']
            doc = dicList[i]['Document']

            dicList[i]['Address'] = add + address
            dicList[i]['Keyword'] = key + keyword
            dicList[i]['Document'] = doc + document


# # check
# for d in dicList:
#     print d


##### misc. #####

# to show all columns in dataframe
#print data.dtypes
# to show type of var
#print type(obc)