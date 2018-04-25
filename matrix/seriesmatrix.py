# coding=utf-8

# import numpy
import pandas
import logging
import datetime

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename='./log/seriesmatrix.log',level=logging.DEBUG,format=LOG_FORMAT, datefmt=DATE_FORMAT)

dfs = pandas.read_csv('./dataset/relation.csv', sep=' ')
date = pandas.read_csv('./dataset/date.csv')
category = pandas.read_csv('./dataset/product.csv',sep=';')

# dfs = dfs[:100000]
idusers_series = dfs['iduser'].value_counts() #pandas.core.series.Series
tmp = list(dfs["iduser"].drop_duplicates())

logging.info("idusers_series.iloc[:].size: "+str(idusers_series.iloc[:].size))
logging.info("list(dfs['iduser'].drop_duplicates()) length:"+str(len(tmp)))
delCount = 0
startTime = datetime.datetime.now()
for index in idusers_series.index:
    count = idusers_series[index]
    if count<10:
        tmp.remove(index)
        delCount+=1
        if delCount<10:
         logging.info("remove "+str(index)+" total "+str(delCount))
endTime = datetime.datetime.now()    
logging.info("del data costs "+str((endTime-startTime).seconds)+" s.")

logging.info("Total delete "+str(delCount)+" user records.")   

dfs = dfs[dfs['iduser'].isin(tmp)]
# logging.info("dfs['iduser'].value_counts():\n "+str(dfs['iduser'].value_counts()))

idusers = dfs['iduser'].drop_duplicates() #去重
# idusers = idusers.sort_values(ascending=True) #排序   取消按照原来顺序
# print(idusers[:100])

'''
将DataFrame类型的iduser和date转化成list
'''
idusers_list = list((idusers))
dates_list = list(date['date'])
category_list = list(category['idcategory'])
product_list = list(category['idproduct'])

# print(category_list[product_list.index(108627)])


row = len(idusers_list)
col = len(dates_list)
logging.info("There are "+str(row)+" users and "+str(col)+" days.")
# 2744 4383(dfs = dfs[:100000]时)
# 144 4383（dfs = dfs[:10000]时）
'''
 创建一个用户数为行，日期数为列的一个数组，value都为0
'''
idcategory =  [[0 for i in range(col)] for i in range(row)]
logging.info('idcategory array  start!')

startTime = datetime.datetime.now()
for index in dfs.index:
    # index:行号
    c_iduser = dfs.loc[index].values[1]
    c_date = dfs.loc[index].values[-1]
    c_idproduct = dfs.loc[index].values[-2]
    c_idcategory = category_list[product_list.index(c_idproduct)]
    # 得到第index行的用户id，产品id，日期
    # 将用户id存入idproduct数组中
    i = idusers_list.index(c_iduser)     
    j = dates_list.index(c_date)
    idcategory[i][j] = c_idcategory
    # logging.info("Now is user "+c_iduser+". Total "+index+" records.")
endTime = datetime.datetime.now()    
logging.info("data idcategory costs "+str((endTime-startTime).seconds)+" s.")

logging.info('idcategory array  finished!')
dff = pandas.DataFrame(data=idcategory, columns=list(date['date']), index=idusers)
# print(dff.head())

dff.to_csv('matrix/series.csv')