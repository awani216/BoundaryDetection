###############################################################################
#------------------Central Driving Module-------------------------------------#
# Author: Awani Mishra                                                        #
# Task  : Wrappers for functionalities provided in this Module                #
#-----------------------------------------------------------------------------#

import argparse
import cv2
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import Adam
import keras.utils
from librosa import load, get_duration
from librosa.feature import mfcc
import numpy as np
import os
import time
from visualAnalysis.templateDetect import findFrames
from audioAnalysis.training import musicTraining
from audioAnalysis.classification import classification
from textualAnalysis.music_intervals import makeMusicSpeechIntervals
from textualAnalysis.commercial_intervals import find_commercials
from textualAnalysis.remove_commercials import remove_commercials
from utils.segment import segmentUsingSegmenetationResults, segmentUsingAnnotations
from utils.dateutil import findShowDate


#------------------------------------------------------------------------------
# Default values declaration

# Path to templates to be used for show detection
templateDir = "../files_used/visualAnalysis/template/"

# Path to audio classification model to be used
defaultModel = "../files_used/audioAnalysis/audioSpeech.h5"

# Path to store audio classification file
audioClassificationFile = "../files_generated/textualAnalysis/audioSpeech.txt"

# Path to store audio Interval File
audioSpeechIntervalFile = "../files_generated/textualAnalysis/musicIntervals.txt"

# Path to store file conta commercial intervals
commercial_extracted_file = "../files_generated/textualAnalysis/commercial_extracted.txt"

# Path to store file which has commercial intervals removed
commercial_removed_file = "../files_generated/textualAnalysis/commercial_removed.txt"

# Path to extracted audio file from video
extracted_wav_file = "../files_generated/audioAnalysis/extracted_sound.wav"

# Default sampling rate for audio analysis
defaultSamplingRate = 22050

# Default break Interval for audio analysis
defaultBreakInterval = 3600

# Default segment length to classify a audio
defaultSegLength     = 1

#------------------------------------------------------------------------------

## Wrapper to call classification function
## For details look int audioAnalysis/classification.py
def classificationWrapper(inputFile, outputFile, modelFile, samplingRate, breakInterval, segLength):
    classification(inputFile, segLength, samplingRate, breakInterval, outputFile, modelFile)

## Wrapper to call training function
## For details look int audioAnalysis/training.py
# Please ensure that the music and speech directories are separate and that the files are
# placed directly inside the folder.
def trainingWrapper(musicDir, speechDir, modelFile, samplingRate, segLength):

    # Listing all music and speech files to be used later for training.
    musicFilesP = os.listdir(musicDir)
    musicFiles = [(musicDir + "/" + i) for i in  musicFilesP]
    speechFilesP = os.listdir(speechDir)
    speechFiles = [(speechDir + "/" + i) for i in  speechFilesP]

    # Calling the main function
    musicTraining(speechFiles, musicFiles, modelFile, segLength, samplingRate)

## Wrapper to call show segmentation function
## For details on the frames recognition fuction, look int visualAnalysis/templateDetect.py
def showSegmentWrapper(videoFile, templateDir, modelFile, skipIntervalsFile, subtitleFile, outputFile):
    if os.path.exists(extracted_wav_file):
        os.remove(extracted_wav_file)
    extractionCommand = "ffmpeg -i " + videoFile + " -ar 22050 -ac 2 " + extracted_wav_file
    os.system(extractionCommand)
    classificationWrapper(extracted_wav_file, audioClassificationFile, defaultModel, defaultSamplingRate,
    defaultBreakInterval, defaultSegLength)
    makeMusicSpeechIntervals(audioClassificationFile, audioSpeechIntervalFile)
    find_commercials(subtitleFile, commercial_extracted_file)
    remove_commercials(commercial_extracted_file, audioSpeechIntervalFile, commercial_removed_file)
    outputDir = "/".join(outputFile.split("/")[:-1])
    matches   = findFrames(videoFile, templateDir, skipIntervalsFile, commercial_removed_file, outputDir, outputFile)
    showDate  = str(findShowDate(videoFile))
    segmentUsingSegmenetationResults(showDate, matches, videoFile, outputDir)

def showSegmentFromAnnotationsWrapper(videoFile, annotationFile, startInd, endInd,
 showNameInd, showDateInd, channelInd, pullDateInd, outputDir):
    segmentUsingAnnotations(videoFile, annotationFile, startInd, endInd, showNameInd,
     showDateInd, channelInd, pullDateInd, outputDir)


# Custom inputs -----------------------------------------------------------------------

# Path to video file
videoFile = "2006-01-10.mp4"

# Path to a file which contains runtime of shows [for faster extraction]
skipIntervalsFile = "skipIntervals.txt"

# Path to subtile file
subtitleFile      = "v.txt"

# Path to Output boundaries
outputFile        = "../files_generated/visualAnalysis/output.txt"

# Directory to output videos segmented
outputDir         = "../files_generated/visualAnalysis/"

annotationFile    = "../files_used/audioAnalysis/datafile_V2 Anna.csv"
startInd    = 7
endInd      = 8
showDateInd = 4
showNameInd = 6
pullDateInd = 2
channelInd  = 5

showSegmentWrapper(videoFile, templateDir, defaultModel, skipIntervalsFile, subtitleFile, outputFile)



###### TODO: Complete the parsing module #####################################
'''

def parse_arguments():
    parser = argparse.ArgumentParser(description="A wrapper script "
                                                 "For boundary detection module")
    tasks = parser.add_subparsers(
        title="subcommands", description="available tasks",
        dest="task", metavar="")

    audioSpeech = tasks.add_parser("audioSpeech",
                                 help="Read a .wav file and classify its seconds as music or speech")
    audioSpeech.add_argument("-i", "--inputFile", required=True, help="Input File")
    audioSpeech.add_argument("-o", "--outputFile", required=True, help="Output Keras Model File")
    audioSpeech.add_argument("-m", "--modelFile", help="classification model to be used", default=defaultModel)
    audioSpeech.add_argument("-sr", "--samplingRate", default=22050, help="sampling rate to be used")
    audioSpeech.add_argument("-b", "--breakInterval", default=3600, help="chunk size to break the audio file into")
    audioSpeech.add_argument("-s", "--segLength", default=1, help="length of intervals for audio classification")

    showSegment = tasks.add_parser("showSegment", help="Read a videoFile and partition it in its show bpundaries")
    showSegment.add_argument("-i", "--inputFile", required=True, help="Input File")
    showSegment.add_argument("-o", "--output", required=True, help="Output File")
    showSegment.add_argument("-m", "--modelFile", help="classification model to be used for audio analysis", default=defaultModel)
    showSegment.add_argument("-td", "--templateDir", help="Directory containing templates", default=templateDir)
    showSegment.add_argument("-st", "--subtitleFile", required=True, help="subtitle file of input video")
    showSegment.add_argument("-si", "--skipInterval", required=True, help="File containing expected length of shows")

    training    = tasks.add_parser("training", help="Train a custom music speech classification model")
    training.add_argument("-md", "--musicDir", required=True, help="Directory containing music files")
    training.add_argument("-sd", "--speechDir", required=True, help="Directory containing speech files")
    audioSpeech.add_argument("-mf", "--model", help="Output Model", default=defaultModel)
    training.add_argument("-sr", "--samplingRate", default=22050, help="sampling rate to be used")
    training.add_argument("-s", "--segLength", default=1, help="length of intervals for audio classification")

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    print(args)
    if (args.tasks == "showSegment"):
        showSegmentWrapper(args.inputFile, args.templateDir, args.modelFile, args.skipInterval, args.subtitleFile, args.output)

    elif (args.tasks == "classification"):
        classificationWrapper(args.inputFile, args.outputFile, args.modelFile, args.samplingRate, args.breakInterval, args.skipInterval)

    elif (args.tasks == "training"):
        trainingWrapper(args.musicDir, args.speechDir, args.model, args.samplingRate, args.segLength)

    else:
        Error("Invalid Task")
'''
