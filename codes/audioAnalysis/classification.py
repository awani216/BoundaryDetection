from librosa import load, get_duration
from librosa.feature import mfcc
import numpy as np
from keras.models import load_model
import time

########## Defining Global Variables ##################################

# file to classify
musicFile = "v2.wav"

# length of intervals for audio classification
segLength = 1

# Sampling Rate of audio (use None for sampling using files sampling rate)
sr = 22050

# Inervals in which large files will be divided
breakInterval = 3600

# File to save the reults in
resultFile = "res.txt"

# File where model is saved
modelFile  = "audioSpeech.h5"

########################################################################

############ Loading Audio File ########################################

def classification(musicFile, segLength, sr, breakInterval, resultFile, modelFile):
    # We divide the audio file in segments of length 3600 secs and load it to data

    data          = []
    audioDuration = get_duration(filename=musicFile) // 1.0
    numSegments   = int(audioDuration // breakInterval)
    print(audioDuration)

    start = time.time()

    for i in range(numSegments):
        st = time.time()
        offset  = i * breakInterval
        y , srp = load(musicFile, sr=sr, duration=breakInterval, offset=offset, res_type='kaiser_fast' )
        for j in range(breakInterval):
            offset = j *  22050
            yp     = y[offset: (offset + sr)]
            D      = np.mean(mfcc(yp, sr=sr, n_mfcc=40), axis=1)
            data.append(D)
        del y
        print(time.time()-st)


    offset   = numSegments * breakInterval
    duration = audioDuration - offset
    y , srp  = load(musicFile, sr=sr, duration=duration, offset=offset, res_type='kaiser_fast' )
    for i in range(int(duration)):
        offset = i *  22050
        yp     = y[offset: (offset + sr)]
        D      = np.mean(mfcc(yp, sr=sr, n_mfcc=40), axis=1)
        data.append(D)
    del y

    data = np.array(data)

    print(time.time() - start)
    model = load_model(modelFile)

    result = np.argmax(model.predict(data), axis=1)

    print(result, result.shape)

    f = open(resultFile, 'w')
    for i in range(result.shape[0]):
        st = str(result[i]) + '\n'
        f.write(st)
    f.close()


classification(musicFile, segLength, sr, breakInterval, resultFile, modelFile)
