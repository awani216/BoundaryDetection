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



#------------------------------------------------------------------
# Default values declaration --------------------------------------

templateDir = "../files_used/visualAnalysis/template/"

defaultModel = "../files_used/audioAnalysis/audioSpeech.h5"

audioClassificationFile = "../files_generated/textualAnalysis/audioSpeech.txt"

audioSpeechIntervalFile = "../files_generated/textualAnalysis/musicIntervals.txt"

commercial_extracted_file = "../files_generated/textualAnalysis/commercial_extracted.txt"

commercial_removed_file = "../files_generated/textualAnalysis/commercial_removed.txt"

extracted_wav_file = "../files_generated/audioAnalysis/extracted_sound.wav"

defaultSamplingRate = 22050

defaultBreakInterval = 3600

defaultSegLength     = 1


def classificationWrapper(inputFile, outputFile, modelFile, samplingRate, breakInterval, segLength):
    classification(inputFile, segLength, samplingRate, breakInterval, outputFile, modelFile)

def trainingWrapper(musicDir, speechDir, modelFile, samplingRate, segLength):
    musicFilesP = os.listdir(musicDir)
    musicFiles = [(musicDir + "/" + i) for i in  musicFilesP]
    speechFilesP = os.listdir(speechDir)
    speechFiles = [(speechDir + "/" + i) for i in  speechFilesP]
    musicTraining(speechFiles, musicFiles, modelFile, segLength, samplingRate)

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
    matchedFramesDir = "/".join(outputFile.split("/")[:-1])
    findFrames(videoFile, templateDir, skipIntervalsFile, commercial_removed_file, matchedFramesDir, outputFile)

# Custom inputs -----------------------------------------------------------------------
videoFile = "v.mp4"
skipIntervalsFile = "skipIntervals.txt"
subtitleFile      = "v.txt"
outputFile        = "../files_generated/visualAnalysis/output.txt"


showSegmentWrapper(videoFile, templateDir, defaultModel, skipIntervalsFile, subtitleFile, outputFile)

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
