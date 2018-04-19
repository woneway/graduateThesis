# _*_ coding: UTF-8 _*_
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
#matplotlib inline
plt.style.use('ggplot')

# columns=['iduser','rating','idproduct','date']
df = pd.read_table('dataset/relation.csv',sep='\s+')
print('print relative.csv head 5')
print(df.head(5))
df = df[:1000]
#print('df.describe()')
#print(df.describe())

print('df.info()')
print(df.info())

pivoted_counts = df.pivot_table(["rating",'idproduct'],index="iduser",columns=['date'],fill_value=0)

print(pivoted_counts.head())
