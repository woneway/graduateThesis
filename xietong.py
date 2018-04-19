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

rating = rating[:20000]

data = rating.pivot_table(index='iduser',columns='idproduct',values='rating') 
#fill_value=0

print('数据规整：输出前5行')
print(data[:5])



'''
计算user之间的相关系数
首先计算min_periods参数
'''

'''
新建一个以 iduser 为行列的方阵 foo，然后挨个填充不同用户间重叠评分的个数：
'''
foo = DataFrame(np.empty((len(data.index),len(data.index)),dtype=int),index=data.index,columns=data.index)

for i in foo.index:
        for j in foo.columns:
            foo.ix[i,j] = data.ix[i][data.ix[j].notnull()].dropna().count()

print('foo1: \n',foo)
for i in foo.index:
        foo.ix[i,i]=0#先把对角线的值设为 0

print('foo: \n',foo)
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

test.ix[790].value_counts(sort=False).plot(kind='bar')
test.ix[1302].value_counts(sort=False).plot(kind='bar')


periods_test = DataFrame(np.zeros((20,7)),columns=[10,20,50,100,200,500,998])

for i in periods_test.index:
        for j in periods_test.columns:
            sample = test.reindex(columns=np.random.permutation(test.columns)[:j])
            periods_test.ix[i,j] = sample.iloc[0].corr(sample.iloc[1])
print(periods_test[:5])

print(periods_test.describe())

'''
std chose 50
'''
check_size = 1000
check = {}
check_data = data.copy()#复制一份 data 用于检验，以免篡改原数据
check_data = check_data.ix[check_data.count(axis=1)>200]#滤除评价数小于200的用户
for user in np.random.permutation(check_data.index):
        movie = np.random.permutation(check_data.ix[user].dropna().index)[0]
        check[(user,movie)] = check_data.ix[user,movie]
        check_data.ix[user,movie] = np.nan
        check_size -= 1
        if not check_size:
            break

corr = check_data.T.corr(min_periods=50)
corr_clean = corr.dropna(how='all')
corr_clean = corr_clean.dropna(axis=1,how='all')#删除全空的行和列
check_ser = Series(check)#这里是被提取出来的 1000 个真实评分
print(check_ser[:5])


result = Series(np.nan,index=check_ser.index)

for user,movie in result.index:#这个循环看着很乱，实际内容就是加权平均而已
        prediction = []
        if user in corr_clean.index:
            corr_set = corr_clean[user][corr_clean[user]>0.1].dropna()#仅限大于 0.1 的用户
        else:continue
        for other in corr_set.index:
            if  not np.isnan(data.ix[other,movie]) and other != user:#注意bool(np.nan)==True
                prediction.append((data.ix[other,movie],corr_set[other]))
        if prediction:
            result[(user,movie)] = sum([value*weight for value,weight in prediction])/sum([pair[1] for pair in prediction])
 

result.dropna(inplace=True)

print('len(result)')
print(len(result))
print('result[:5]')
print(result[:5])
print('result.corr(check_ser.reindex(result.index))')
print(result.corr(check_ser.reindex(result.index)))
print('推荐期望与实际评价之差的绝对值')
print((result-check_ser.reindex(result.index)).abs().describe())#推荐期望与实际评价之差的绝对值

'''
realize
'''
corr = data.T.corr(min_periods=50)
corr_clean = corr.dropna(how='all')
corr_clean = corr_clean.dropna(axis=1,how='all')
lucky = np.random.permutation(corr_clean.index)[0]
gift = data.ix[lucky]
gift = gift[gift.isnull()]#现在 gift 是一个全空的序列

corr_lucky = corr_clean[lucky].drop(lucky)#lucky 与其他用户的相关系数 Series，不包含 lucky 自身
corr_lucky = corr_lucky[corr_lucky>0.1].dropna()#筛选相关系数大于 0.1 的用户
for movie in gift.index:#遍历所有 lucky 没看过的电影
        prediction = []
        for other in corr_lucky.index:#遍历所有与 lucky 相关系数大于 0.1 的用户
            if not np.isnan(data.ix[other,movie]):
                prediction.append((data.ix[other,movie],corr_clean[lucky][other]))
        if prediction:
            gift[movie] = sum([value*weight for value,weight in prediction])/sum([pair[1] for pair in prediction])
 
print(gift.dropna().order(ascending=False))#将 gift 的非空元素按降序排列
