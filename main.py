import pandas as pd
import numpy as np

# variables
authorDict = []
tempList = []

# import data
data = pd.read_csv('dataset.csv')
#print data.dtypes

# extract information from data
authorList = data['Authors with affiliations'].str.split(';')
indexList = data['Index Keywords'].str.split(';')

# print type(authorList)
# print type(authorList[0])
# print len(authorList[0])
# print authorList[0]
# print authorList[0][0]
# print authorList[0][1]
# print authorList[0][2]
# print authorList[0][3]
# print authorList[0][4]
# print authorList[0][5]


for i in range(len(authorList)-2500):
    #tempList = [text.split() for text in authorList[i] if text]
    #print tempList
    for j in range(len(authorList[i])):
        tempList = authorList[i][j].split('.,')
        # print type(tempList[0])
        # print tempList[0]
        # print tempList[1]
        authorDict.append({'Author': tempList[0], 'Address': tempList[1] if len(tempList) > 1 else ''})

print authorDict[1]
print authorDict[2]
# for i in authorList:
#     authorDict.append({'Author': i, 'Location': i[1]})
#     print i





##### misc. #####

# to show all columns in dataframe
#print data.dtypes
# to show type of var
#print type(obc)