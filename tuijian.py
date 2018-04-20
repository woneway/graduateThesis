import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Embedding,Dropout,Dense,Merge
from keras.layers.core  import Reshape

k = 128
rating = pd.read_csv('dataset/relation.csv',sep="\s+")
print(rating.head())
rating = rating[:50000]
n_users = np.max(rating['iduser'])
n_products = np.max(rating['idproduct'])
print(n_users,n_products,len(rating))

plt.hist(rating['rating'])
plt.show()
print(np.mean(rating['rating']))

model1 = Sequential()
model1.add(Embedding(n_users+1,k,input_length=1))
model1.add(Reshape((k,)))

model2 = Sequential()
model2.add(Embedding(n_products+1,k,input_length=1))
model2.add(Reshape((k,)))

model = Sequential()
model.add(Merge([model1,model2],mode = 'dot',dot_axes = 1))

model.compile(loss='mse',optimizer='adam')

users = rating['iduser'].values
products = rating['idproduct'].values

train_X = [users,products]
train_Y = rating['rating'].values

model.fit(train_X,train_Y,batch_size = 100,epochs=50)
i = 182
j = 99

pred = model.predict([np.array([users[i]]),np.array([products[j]])])

sum = 0
for i in range(rating.shape[0]):
	sum+=(rating['rating'][i] - model.predict([np.array([users[i]]),np.array([products[j]])])) ** 2

mse = math.sqrt(sum/rating.shape[0])
print(mse)
