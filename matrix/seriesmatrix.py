# coding=utf-8

# import numpy
import pandas

dfs = pandas.read_csv('./dataset/relation.csv', sep=' ')
date = pandas.read_csv('./dataset/date.csv')
dfs = dfs[:10000]
idusers = dfs['iduser'].drop_duplicates() #去重
# idusers = idusers.sort_values(ascending=True) #排序   取消按照原来顺序
# print(idusers[:100])

'''
将DataFrame类型的iduser和date转化成list
'''
idusers_list = list((idusers))
dates_list = list(date['date'])

row = len(idusers_list)
col = len(dates_list)
print(row," ",col)
# 2744 4383(dfs = dfs[:100000]时)
# 144 4383（dfs = dfs[:10000]时）
'''
 创建一个用户数为行，日期数为列的一个数组，value都为0
'''
idproduct =  [[0 for i in range(col)] for i in range(row)]

for index in dfs.index:
    # index:行号
    c_iduser = dfs.loc[index].values[1]
    c_date = dfs.loc[index].values[-1]
    c_idproduct = dfs.loc[index].values[-2]
    # 得到第index行的用户id，产品id，日期
    # 将用户id存入idproduct数组中
    i = idusers_list.index(c_iduser)     
    j = dates_list.index(c_date)
    idproduct[i][j] = c_idproduct
    # print(i," " ,j," ",c_idproduct)


dff = pandas.DataFrame(data=idproduct, columns=list(date['date']), index=idusers)
print(dff.head())

dff.to_csv('matrix/serise.csv')