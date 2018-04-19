# _*_ coding: UTF-8 _*_
import pandas as pd
from pandas import Series,DataFrame
import numpy as np
import matplotlib.pyplot as plt

'''
协同过滤
'''
rating = pd.read_table('dataset/relation.csv',sep='\s+')
print('输出数据集前三行 rating[:3]')
print(rating[:3])

rating = rating[:10000]

data = rating.pivot_table(index='iduser',columns='idproduct',values='rating') 
#fill_value=0

print('数据规整：输出前5行')
print(data[:5])

foo = DataFrame(np.empty((len(data.index),len(data.index)),dtype=int),index=data.index,columns=data.index)
print('foo.index: ',foo.index)
print('foo.columns: ',foo.columns)
for i in foo.index:
        for j in foo.columns:
            foo.ix[i,j] = data.ix[i][data.ix[j].notnull()].dropna().count()

for i in foo.index:
        foo.ix[i,i]=0#先把对角线的值设为 0

print('foo: ',foo)
ser = Series(np.zeros(len(foo.index)))


print('ser: \n',ser)
for i in foo.index:
        ser[i]=foo[i].max()#计算每行中的最大值
print('ser: \n',ser)
maxline = ser.idxmax()
print('ser的最大值所在的行号: ',maxline)

print('最大值: ',ser[maxline])

maxline2 = foo[foo==ser[maxline]][maxline].dropna()
print('ser的最大值所在的行号：',foo[foo==ser[maxline]][maxline])


print('相关系数: ',data.ix[790].corr(data.ix[1302]))


test = data.reindex([790,1302],columns=data.ix[790][data.ix[1302].notnull()].dropna().index)

print(test)

test.ix[424].value_counts(sort=False).plot(kind='bar')
test.ix[4169].value_counts(sort=False).plot(kind='bar')
