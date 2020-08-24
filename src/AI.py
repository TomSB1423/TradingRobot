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


# Fetch IBM
print("Fetching IBM stock data from Yahoo Finance...")
df = web.DataReader('IBM', data_source='yahoo', start='1998.01.02', end='2020.08.14')
print(f"Downloaded {len(df)} data points")
print(f"Date range: {df.index[0]} to {df.index[-1]}")

if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

plt.figure(figsize=(16,8))
plt.title('IBM Historical Stock Prices', fontsize=16, fontweight='bold')
plt.xlabel('Date')
plt.ylabel('Close Price (USD)')
plt.plot(df['Close'])
plt.show()
print(df.head(), df.shape)

# Create dataset
print("Preparing dataset...")
data = df[['Close']].copy()
dataset = data.values
trainingDataLen = int(np.ceil(len(dataset) * 0.8))
print(f"Training data: {trainingDataLen} samples ({trainingDataLen/len(dataset)*100:.1f}%)")
print(f"Test data: {len(dataset) - trainingDataLen} samples ({(len(dataset) - trainingDataLen)/len(dataset)*100:.1f}%)")

# Scaling
scaler =  MinMaxScaler(feature_range=(0,1))
scaledData = scaler.fit_transform(dataset)
print("Data normalized to range [0, 1]")

# Flip data
trainingData = scaledData[0:trainingDataLen, :]
testData = scaledData[trainingDataLen - 60:, :]

# Training
# Split data into Input and Output
print("Creating training sequences...")
xTrain = []
yTrain = []

for i in range(60, len(trainingData)):
  xTrain.append(trainingData[i-60:i, 0])
  yTrain.append(trainingData[i, 0])

# Convert to numpy array
xTrain, yTrain = np.array(xTrain), np.array(yTrain)
xTrain = np.reshape(xTrain, (xTrain.shape[0], xTrain.shape[1], 1))
print(f"Training sequences shape: {xTrain.shape}")

# Test
# Split data into Input and Output
xTest = []
yTest = dataset[trainingDataLen:, :]
for i in range(60, len(testData)):
  xTest.append(testData[i-60:i, 0])
  
xTest = np.array(xTest)
xTest = np.reshape(xTest, (xTest.shape[0], xTest.shape[1], 1))
print(f"Test sequences shape: {xTest.shape}")

# Create model
print("Building and training LSTM model...")
model = keras.Sequential([
    keras.layers.LSTM(50, input_shape=(xTrain.shape[1],1)),
    keras.layers.Dense(50),
    keras.layers.Dense(25),
    keras.layers.Dense(1)
])

#Show model summary
model.summary()

print("Training model (this may take a while)...")
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(xTrain, yTrain, epochs=1, batch_size=1, verbose=1)
print("Model training complete")

# Evaluation
print("Evaluating model performance...")
Prediction = model.predict(xTest)
Prediction = scaler.inverse_transform(Prediction)
rmse = np.sqrt(np.mean((Prediction - yTest)**2))
print('=' * 50)
print(f'Root Mean Square Error (RMSE): ${rmse:.2f}')
print('=' * 50)

train = data[:trainingDataLen]
valid = data[trainingDataLen:]
valid['Prediction'] = Prediction

plt.figure(figsize=(16,8))
plt.title('IBM Stock Price: Actual vs Predicted', fontsize=16, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Close Price IBM (USD)', fontsize=12)
plt.plot(valid[['Close', 'Prediction']])
plt.legend(['True price', 'Prediction'], fontsize=12)
plt.grid(True, alpha=0.3)
plt.show()