from math import sqrt
from numpy import concatenate
from matplotlib import pyplot
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

# load dataset
dataset = read_csv('matrix/serise.csv',index_col=0)
# 不取值userid
values = dataset.values
# print(values)
# ensure all data is float
values = values.astype('float32')
# normalize features
scaler = MinMaxScaler(feature_range=(0, 1))
values = scaler.fit_transform(values)
# DataFrame(values).to_csv("dd.csv")
n_train = 2544
train = values[:n_train, :]
# print(train)
test = values[n_train:, :]
# print(test)
# split into input and outputs
train_X, train_y = train[:, :-875], train[:, -876:-1]
test_X, test_y = test[:, :-875], test[:,-876:-1]
# print(train_X.shape,train_y.shape)
# print(test_X.shape,test_y.shape)
# train_X.shape[0] 行数
# train_X.shape[1] 列数
# (120, 3508) (120, 875)


# reshape input to be 3D [samples, timesteps, features]
train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
# print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)
# (120, 1, 3506) (120, 875) (24, 1, 3506) (24, 875)

# design network
model = Sequential()
model.add(LSTM(128,input_shape=(train_X.shape[1],train_X.shape[2])))
model.add(Dense(875))
model.compile(loss='mae', optimizer='adam')
# fit network
history = model.fit(train_X, train_y, epochs=50, batch_size=40, validation_data=(test_X, test_y), verbose=2, shuffle=False)
# plot history
# pyplot.plot(history.history['loss'], label='train')
# pyplot.plot(history.history['val_loss'], label='test')
# pyplot.legend()
# pyplot.show()
 
# make a prediction
yhat = model.predict(test_X)
print(yhat.shape)
test_X = test_X.reshape((test_X.shape[0], test_X.shape[2]))
print(test_X.shape)
# invert scaling for forecast
inv_yhat = concatenate((test_X[:, :],yhat), axis=1)
print(inv_yhat.shape)
inv_yhat = scaler.inverse_transform(inv_yhat)
inv_yhat = inv_yhat[:,-876:]
# invert scaling for actual
test_y = test_y.reshape((len(test_y), 875))
inv_y = concatenate(( test_X[:, :],test_y), axis=1)
inv_y = scaler.inverse_transform(inv_y)
inv_y = inv_y[:,-875:]
# calculate Accurancy

pyplot.plot(inv_yhat[-2],label="predict")
pyplot.plot(inv_y[-2],label="actual")
pyplot.legend()
pyplot.show()