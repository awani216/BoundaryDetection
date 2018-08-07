from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import Adam
import keras.utils
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import glob
import time
from sklearn.preprocessing import LabelEncoder
import np_utils
import h5py


########## Defining Global Variables ######################

# list of all speech files
speechFiles = glob.glob("./speech/*")

# list of all music files
musicFiles = glob.glob("./music/**/*.mp3")

# length of intervals for audio classification
segLength = 1

# Sampling Rate of audio (use None for sampling using files sampling rate)
sr = 22050

def makeData (fl, label):
    try:
        print(fl)
        audioDuration = (librosa.get_duration(filename=fl) // 1.0) - 1
        numSegments = int(audioDuration // segLength)
        data = []
        if(audioDuration > 100):
            audioDuration = 100.0
            numSegments   = 100
        y , srp   = librosa.load(fl, sr=sr, duration=audioDuration, res_type='kaiser_fast')
        print(audioDuration , y.shape)     
        for i in range(numSegments - 1):
            offset    = i*sr
            yp        = y [offset:(offset+sr)]
            D         = librosa.feature.mfcc(yp, sr=sr, n_mfcc=40)
            D         = np.mean(D, axis=1)
            D         = np.append(D, label)
            data.append(D)

        return data
    except Exception as e:
        print("Error encountered while parsing file: ", fl)
        return []

dataset = []

for i in speechFiles:
    dataset = dataset + makeData(i, 0)

for i in musicFiles:
    dataset = dataset + makeData(i,1)

dataset = np.array(dataset)

datasetLen = len(dataset)

print(datasetLen)
perm = np.random.permutation(datasetLen)

dataset = dataset[perm]

X = dataset[:-200, :-1]
Y = dataset[:-200, -1]

valX = dataset[-200: , :-1]
valY = dataset[-200: , -1]

print(X.shape, Y.shape, valX.shape, valY.shape)
lb = LabelEncoder()

Y = keras.utils.to_categorical(lb.fit_transform(Y))
valY = keras.utils.to_categorical(lb.fit_transform(valY))

nLabels = 2
filter_size = 2

# build model
model = Sequential()

model.add(Dense(256, input_shape=(40,)))
model.add(Activation('relu'))
model.add(Dropout(0.5))

model.add(Dense(256))
model.add(Activation('relu'))
model.add(Dropout(0.5))

model.add(Dense(nLabels))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')
model.fit(X,Y, batch_size=128, epochs=1000, validation_data=(valX, valY))

model.save("audioSpeech.h5")
