# _*_ coding:UTF-8 _*_
from pandas import read_csv
from datetime import datetime
'''
对原始数据进行处理，得到
182,4,43286
182,4,14016
182,5,113
182,2,43287
182,5,381
类型的数据，不要表头【iduser,rating,idproduct】
'''
dataset = read_csv('dataset/review.csv',index_col=1)
dataset.drop('idreview',axis=1,inplace=True)
dataset.drop('review_rating',axis=1,inplace=True)
dataset.drop('date',axis=1,inplace=True)
dataset.to_csv('xietong_filter/xietong.csv',header=None)