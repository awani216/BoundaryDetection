#/-------------------------------------------------------------------------\
#/ Audio training module                                                   \
#/ Author : Awani Mishra                                                   \
#/ Redhen Labs                                                             \
#/ Project : Show Segmentation                                             \
#/ Objective : Train a machine learning kernel to detect and calssify audio\ 
#/ input as music or speech.                                               \
#/-------------------------------------------------------------------------\

import os
import numpy as np
import sklearn
import librosa as lr
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import Adam
from keras.utils import np_utils
from sklearn import metrics
from sklearn.preprocessing import LabelEncoder

# Defining varibles
 
# Path to directory containing music files
musicPath

# Path to directory containing speech files
speechPath

# Sampling rate (for music files)
samplingRate

# Sample Duration duration
samplingDuration

musicFiles  = os.listdir(musicPath) 
speechFiles = os.listdir(speechPath)

#-----------------\
# Data Extraction \
#-----------------\

def extractDataFromFile(filepath, label):
    fileDuration = ls.get_duration(filepath)
    numSegments = filesDuration // samplingDuration
    data = []
    for i in range(numSegments)
        toffset = i * duration
        tdata, wt = lr.load(filepath, sr=samplingRate, offset=toffset, duration=samplingDuration)
        mfccs = np.mean(librosa.feature.mfcc(y=tdata, sr=samplingRate, n_mfcc=40).T,axis=0)
        mfccs.append(label)
        data.append(mfccs)
    return data

dataset = []

for i in musicFiles:
    data = extractDataFromFile(i, 0)
    dataset.append(data)

for i in speechFiles:
    data = extractDataFromFile(i, 1)
    dataset.append(data)

#--------------------\
# Data Training      \ 
#--------------------\

numberCols = length(dataset[0])
X = dataset[:, :-1]
y = dataset[:, numberCols-1]

lb = LabelEncoder()

y = np_utils.to_categorical(lb.fit_transform(y))

num_labels = y.shape[1]
filter_size = 2

# build model
model = Sequential()

model.add(Dense(256, input_shape=(40,)))
model.add(Activation('relu'))
model.add(Dropout(0.5))

model.add(Dense(256))
model.add(Activation('relu'))
model.add(Dropout(0.5))

model.add(Dense(num_labels))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')

model.fit(X, y, batch_size=32, epochs=5, validation_data=(val_x, val_y))
