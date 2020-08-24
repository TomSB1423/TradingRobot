# TensorFlow and tf.keras
from tensorflow import keras
# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
from sklearn.preprocessing import MinMaxScaler
# pyplot style
plt.style.use('fivethirtyeight')

# Fetch stock IBM from yfinance
df = web.DataReader('IBM', data_source='yahoo', start='1998.01.02', end='2020.08.14')
plt.figure(figsize=(16,8))
plt.plot(df['Close'])
plt.show()
print(df.head(), df.shape)

# Create dataset
data = df.filter(['Close'])
dataset = data.values
trainingDataLen = int(np.ceil(len(dataset) * 0.8))
# Scaling
scaler =  MinMaxScaler(feature_range=(0,1))
scaledData = scaler.fit_transform(dataset)

# Flip data
trainingData = scaledData[0:trainingDataLen, :]
testData = scaledData[trainingDataLen - 60:, :]

# Training
# Split data into Input and Output
xTrain = []
yTrain = []

for i in range(60, len(trainingData)):
  xTrain.append(trainingData[i-60:i, 0])
  yTrain.append(trainingData[i, 0])

# Convert to numpy array
xTrain, yTrain = np.array(xTrain), np.array(yTrain)
xTrain = np.reshape(xTrain, (xTrain.shape[0], xTrain.shape[1], 1))

# Test
# Split data into Input and Output
xTest = []
yTest = dataset[trainingDataLen:, :]
for i in range(60, len(testData)):
  xTest.append(testData[i-60:i, 0])
  
xTest = np.array(xTest)
xTest = np.reshape(xTest, (xTest.shape[0], xTest.shape[1], 1))

# Create model
model = keras.Sequential([
    keras.layers.LSTM(50, input_shape=(xTrain.shape[1],1)),
    keras.layers.Dense(50),
    keras.layers.Dense(25),
    keras.layers.Dense(1)
])

#Show model summary
model.summary()

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(xTrain, xTrain, epochs=1, batch_size=1)

# Evaluation
Prediction = model.predict(xTest)
Prediction = scaler.inverse_transform(Prediction)
rmse = np.sqrt(np.mean(Prediction - yTest)**2)
print('Root mean square: ', rmse)

train = data[:trainingDataLen]
valid = data[trainingDataLen:]
valid['Prediction'] = Prediction
plt.figure(figsize=(16,8))
plt.xlabel('Date')
plt.ylabel('Close Price IBM')
plt.plot(valid[['Close', 'Prediction']])
plt.legend(['True price', 'Prediction'])
plt.show()