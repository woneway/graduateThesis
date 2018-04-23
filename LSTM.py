import numpy as np
import pandas as pd

df = pd.read_table('dataset/relation.csv',sep=' ')
date = pd.read_csv('dataset/date.csv')
df = df[:10000]

dff = pd.DataFrame(data=df['idproduct'],index=df['iduser'],columns=df['date'])
print(dff.head())