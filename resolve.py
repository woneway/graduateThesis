# _*_ coding: UTF-8 _*_
from pandas import read_csv
from datetime import datetime

dataset = read_csv('dataset/review.csv',index_col=1)
print("原始数据前五行：")
print(dataset.head(5))
dataset.drop('idreview',axis=1,inplace=True)
dataset.drop('review_rating',axis=1,inplace=True)
print("idreview，review_rating删除后：")
print(dataset.head(5))

dataset.to_csv('dataset/relation.csv',sep=' ')
