import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as data
from keras.models import load_model
import streamlit as st

start = '2015-01-01'
end = '2021-12-31'

st.title('STOCK TREND PREDICTION')
user_input = st.text_input('Enter Stock Ticker', 'MSFT')
dataF = data.DataReader(user_input, 'yahoo', start, end)

#Describing the data

st.subheader('Data from 2015 to 2021')
st.write(dataF.describe())

#Visualizations
st.subheader('CLOSING PRICE V TIME CHART')
fig = plt.figure(figsize=(15, 5))
plt.plot(dataF.Close)
st.pyplot(fig)

st.subheader('CLOSING PRICE V TIME CHART WITH 100MA')
ma100 = dataF.Close.rolling(100).mean()
fig = plt.figure(figsize=(15, 5))
plt.plot(ma100)
plt.plot(dataF.Close)
st.pyplot(fig)

st.subheader('CLOSING PRICE V TIME CHART WITH 100MA & 200MA')
ma100 = dataF.Close.rolling(100).mean()
ma200 = dataF.Close.rolling(200).mean()
fig = plt.figure(figsize=(15, 5))
plt.plot(ma100, 'r')
plt.plot(ma200, 'b')
plt.plot(dataF.Close, 'g')
st.pyplot(fig)

#Dividing the data into Training and Testing
Training_data = pd.DataFrame(dataF['Close'][0:int(len(dataF)*0.70)])
Testing_data = pd.DataFrame(dataF['Close'][int(len(dataF)*0.70): int(len(dataF))])

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_ranger = (0, 1))

data_training_array = scaler.fit_transform(Training_data)

#Splitting Data into a_train and b_train
a_train = []
b_train = []

for val in range(100, data_training_array.shape[0]):
    a_train.append(data_training_array[val-100: val])
    b_train.append(data_training_array[val, 0])

a_train, b_train = np.appray(a_train), np.array(b_train)

#Load Model
model = load_model('keras_model.h5')

#Model Testing
past_100_days = data_training.tail(100)
final_dataF = past_100_days.append(data_testing, ignore_index = True)
input_data = scaler.fit_transform(final_dataF)

a_test = []
b_test = []

for val in range(100, input_data.shape[0]):
    a_test.append(input_data[val-100: val])
    b_test.append(input_data[val, 0])

#Testing Data
a_test, b_test = np.array(a_test), np.array(b_test)
b_prediction = model.predict(a_test)
scaler = scaler.scale_
scale_factor = 1/scaler[0]
b_prediction = b_prediction* scale_factor
b_test = b_test* scale_factor


#Graph Representation
st.subheader('PREDICTION V ACTUAL PRICE')
fig1 = plt.figure(figsize=(15, 5))
plt.plot(b_test, 'v', label = 'Actual Price')
plt.plot(b_prediction, 'r', label = 'Predicted Price')
plt.xlabel('Time')
plt.xlabel('Price')
plt.legend()
st.pyplot(fig1)


