# _*_ coding:UTF-8 _*_
from pandas import read_csv
import numpy as np
'''
review表中时间范围:1999/7/1~2011/6/16
生成一个行再1999/7/1～2011/6/16的表
'''
df = read_csv('dataset/date.csv')
print(df)