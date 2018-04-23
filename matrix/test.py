# coding=utf-8

# import numpy
import pandas

dfs = pandas.read_csv('./dataset/relation.csv', sep=' ')
date = pandas.read_csv('./dataset/date.csv')
dfs = dfs[:100]
idusers = dfs['iduser'].drop_duplicates() #去重
# idusers = idusers.sort_values(ascending=True) #排序   取消按照原来顺序
# print(idusers[:100])

idproduct = [[] for i in range(len(idusers))]
# print(idproduct[:15])
tempdate = [{} for i in range(len(idusers))]
k = 0
for i in idusers.index:
    for index in dfs.index:
        c_iduser = dfs.loc[index].values[1:2]
        c_date = dfs.loc[index].values[-1]
        c_idproduct = dfs.loc[index].values[-2:-1]
        l_iduser = idusers.loc[i]
        # print(c_iduser," " ,c_date," ",c_idproduct," ",l_iduser)
        if c_iduser == l_iduser:
              tempdate[k][c_date] = c_idproduct
              k+=1

print(tempdate)

for i in range(len(idusers)):
    for d in date['date']:
        if d in tempdate[i].keys():
            idproduct[i].append(int(tempdate[d]))
        else:
            idproduct[i].append(0)

dff = pandas.DataFrame(data=idproduct, columns=list(date['date']), index=idusers)
print(dff.head())