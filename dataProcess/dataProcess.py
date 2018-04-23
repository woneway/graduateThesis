# _*_ coding:UTF-8 _*_
from pandas import read_csv
from datetime import datetime
'''
           
    date          iduser  rating  idproduct
0   2001/6/21     182       4      43286
1   2001/6/4      182       4      14016
2   2001/5/16     182       5        113
3   2001/5/4      182       2      43287
4   2001/3/7      182       5        381

csv中：
date iduser rating idproduct
2001/6/21 182 4 43286
2001/6/4 182 4 14016
2001/5/16 182 5 113
2001/5/4 182 2 43287
2001/3/7 182 5 381
2001/3/2 182 5 43288
'''
dataset = read_csv('dataset/review.csv')
dataset.drop('idreview',axis=1,inplace=True)
dataset.drop('review_rating',axis=1,inplace=True)
# dataset = dataset.sort_values(by="iduser",ascending=True)
dataset.to_csv('dataset/relation.csv',sep=' ')