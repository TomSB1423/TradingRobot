# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
# Input data here

adjusted = os.path.expanduser('~/Documents/Programming/Trading Robot/Ai/rawData/IBM_adjusted.txt')

df = pd.read_csv(adjusted, names=['Date', 'Time', 'Open'], usecols=[0,1,2])
df = df[0::20]
df["Date"] = df["Date"] + ' ' + df["Time"]
df.drop(columns=['Time'])

# Create model
model = keras.Sequential([
    keras.layers.Dense(50, activation='relu', input_shape=(30,)),
    keras.layers.Dense(50, activation='relu'),
    keras.layers.Dense(1)
])

model.summary()
input("Press Enter to train...")

# Model compiler
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
              

# Fit the data points
model.fit(trainingData, trainingLables, epochs=10)

# Evaluate results
test_loss, test_acc = model.evaluate(testData,  testLables, verbose=2)

print('\nTest accuracy:', test_acc)