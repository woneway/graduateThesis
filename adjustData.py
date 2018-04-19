# _*_ coding: UTF-8 _*_
from pandas import read_csv
from datetime import datetime

'''
将日期2011-1-1转换为20110101
'''
def date2number(x):
    x = datetime.strptime(x, '%Y/%m/%d')
    return x.strftime('%Y%m%d')
dataset = read_csv('dataset/review.csv',index_col=1)
print("原始数据前五行：")
print(dataset.head(5))
dataset.drop('idreview',axis=1,inplace=True)
dataset.drop('review_rating',axis=1,inplace=True)
print("idreview，review_rating删除后：")
print(dataset.head(5))

dataset['date'] = dataset['date'].apply(date2number)
print(dataset.head(5))
dataset.to_csv('dataset/relation.csv',sep=' ')
