import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd


adjusted = os.path.expanduser('~/Documents/Programming/Trading Robot/Ai/rawData/IBM_adjusted.txt')
unadjusted = os.path.expanduser('~/Documents/Programming/Trading Robot/Ai/rawData/IBM_unadjusted.txt')
savePath = os.path.expanduser('~/Documents/Programming/Trading Robot/Ai/editedData/data.txt')

df = pd.read_csv(adjusted, names=['Date', 'Time', 'Open'], usecols=[0,1,2])

df.to_csv(path_or_buf=savePath)

input("plot data?")

df["Date"] = df["Date"] + ' ' + df["Time"]
df.drop(columns=['Time'])

date_time = pd.to_datetime(df.pop('Date'), format='%m/%d/%Y %H:%M')
plot_cols = ['Open']
plot_features = df[plot_cols]
plot_features.index = date_time
_ = plot_features.plot(subplots=True)


# df = pd.read_csv(unadjusted, names=['Date', 'Time', 'Open'], usecols=[0,1,2])
# df = df[0::20]
# df["Date"] = df["Date"] + ' ' + df["Time"]
# df.drop(columns=['Time'])

# date_time = pd.to_datetime(df.pop('Date'), format='%m/%d/%Y %H:%M')
# plot_cols = ['Open']
# plot_features = df[plot_cols]
# plot_features.index = date_time
# _ = plot_features.plot(subplots=True)
print('Plotting...')
plt.show()