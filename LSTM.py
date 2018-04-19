import numpy
import matplotlib.pyplot as plt
from pandas import read_csv
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

"""
LSTM 相当于RNN的一种改进
A say: go to NanJing at 4.19
model learn ---> NanJing is a dest 4.19 is a date
But now B say : leaving NanJing at 4.19
model learn ---> NanJing is a dest 4.19 is a date ---> but NanJing is a start 
神经网络就是 同样的input给出同样的output
于是就有了RNN 看前一个词来 给加强训练
而LSTM 就是 看前面时间的行为 来分析行为 
0：  182 4 14016 2001/6/4
感觉就是 当前时间 6.14 查看前三个时间 得到用户182的行为都为评价4，评论都为UnHelpful
那这次的用户行为 评价 可能为3 
训练完之后就能预测 就是用户兴趣发现。。？
"""

dataframe = read_csv('./data/relation.csv')
dataset numpy.ndarray type
dataset numpy.ndarray[i] str type
"""
划分数据集 读进来是字符串 LSTM模型需要接受float
比如2001/6/21 按照你的想法转换为数值
"""


def create_dataset(dataset, look_back=3):
    """
    :param dataset: 原始数据集 划分为 X 翰 Y
    :param look_back: 输出数据与 look_back 个 之前的输入数据有关联
    :return: 划分好的 X 翰 Y
    data_X, data_Y = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        data_X.append(a)
        data_Y.append(dataset[i + look_back, 0])
    return numpy.array(data_X), numpy.array(data_Y)
    """
    pass


scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)

train_size = int(len(dataset) * 0.67)
test_size = len(dataset) - train_size
train, test = dataset[0: train_size, :], dataset[train_size:len(dataset), :]

look_back = 3
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)

trainX = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

# 模型搭建
model = Sequential()
model.add(LSTM(4, input_shape=(1, look_back)))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(trainX, trainY, epochs=100, batch_size=1, verbose=2)

trainPredict = model.predict(trainX)
testPredict = model.predict(testX)

trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testY])

# 计算误差 绘图
trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:,0]))

trainPredictPlot = numpy.empty_like(dataset)
trainPredictPlot[:, :] = numpy.nan
trainPredictPlot[look_back:len(trainPredict)+look_back, :] = trainPredict

testPredictPlot = numpy.empty_like(dataset)
testPredictPlot[:, :] = numpy.nan
testPredictPlot[len(trainPredict)+(look_back*2)+1:len(dataset)-1, :] = testPredict

plt.plot(scaler.inverse_transform(dataset))
plt.plot(trainPredictPlot)
plt.plot(testPredictPlot)
plt.show()




