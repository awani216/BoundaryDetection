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
from utils.dateTimeUtil import findShowDate


########### Default Values declaration  #######################################
# You can either specify these from commandline or input them here

# Path to templates to be used for show detection
defaultTemplateDir = "../files_used/visualAnalysis/template/"

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

# Path to input audio for classification
defaultAudioFile = ""

# Path to default Model output
defaultClassificationFile = ""

# Path to audio classification model to be used
defaultModel           = "../files_used/audioAnalysis/audioSpeech.h5"

# Default sampling rate for audio analysis
defaultSamplingRate    = 22050

# Default break Interval for audio analysis
defaultBreakInterval   = 3600

# Default segment length to classify a audio
defaultSegLength       = 1

# Default Music Directory
defaultMusicDir        = ""

# Default Speech Directory
defaultSpeechDir       = ""

# Default Output keras moder file
defaultOutputModelFile = ""

# Path to video file
defaultVideoFile = "2006-01-10.mp4"

# Path to a file which contains runtime of shows [for faster extraction]
defaultSkipIntervalsFile = "skipIntervals.txt"

# Path to subtile file
defaultSubtitleFile      = "st.txt"

# Path to Output boundaries
defaultBoundaryFile        = "../files_generated/visualAnalysis/output.txt"

# Directory to output videos segmented
defaultSegmentationDir         = "../files_generated/visualAnalysis/"

# Default values of some parameters for show segmentation using annotations
# Look into utils/segment.py for more information
defaultAnnotationFile = "ann.csv"
defaultStartInd       = 7
defaultEndInd         = 8
defaultShowDateInd    = 4
defaultShowNameInd    = 6
defaultPullDateInd    = 2
defaultChannelInd     = 5
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
def showSegmentWrapper(videoFile, templateDir, modelFile, skipIntervalsFile, subtitleFile, outputFile, outputDir):
    if os.path.exists(extracted_wav_file):
        os.remove(extracted_wav_file)
    extractionCommand = "ffmpeg -i " + videoFile + " -ar 22050 -ac 2 " + extracted_wav_file
    os.system(extractionCommand)
    classificationWrapper(extracted_wav_file, audioClassificationFile, defaultModel, defaultSamplingRate,
    defaultBreakInterval, defaultSegLength)
    makeMusicSpeechIntervals(audioClassificationFile, audioSpeechIntervalFile)
    find_commercials(subtitleFile, commercial_extracted_file)
    remove_commercials(commercial_extracted_file, audioSpeechIntervalFile, commercial_removed_file)
    matches   = findFrames(videoFile, templateDir, skipIntervalsFile, commercial_removed_file, outputDir, outputFile)
    showDate  = str(findShowDate(videoFile))
    segmentUsingSegmenetationResults(showDate, matches, videoFile, outputDir)

def showSegmentFromAnnotationsWrapper(videoFile, annotationFile, startInd, endInd,
 showNameInd, showDateInd, channelInd, pullDateInd, outputDir):
    segmentUsingAnnotations(videoFile, annotationFile, startInd, endInd, showNameInd,
     showDateInd, channelInd, pullDateInd, outputDir)



###### Input Parser ###########################################################
def parse_arguments():
    parser = argparse.ArgumentParser(description="A wrapper script "
                                             "For boundary detection module")
    tasks = parser.add_subparsers(
        title="subcommands", description="available tasks",
        dest="tasks", metavar="")

    audioSpeech = tasks.add_parser("classification",
            help="Read a .wav file and classify its seconds as music or speech")
    audioSpeech.add_argument("-i", "--inputFile",
            default=defaultAudioFile, help="Input File")
    audioSpeech.add_argument("-o", "--outputFile",
            default=defaultClassificationFile, help="Output classification File")
    audioSpeech.add_argument("-m", "--modelFile",
            default=defaultModel, help="classification model to be used")
    audioSpeech.add_argument("-sr", "--samplingRate",
            default=defaultSamplingRate, help="sampling rate to be used")
    audioSpeech.add_argument("-b", "--breakInterval",
            default=defaultBreakInterval,
            help="chunk size to break the audio file into")
    audioSpeech.add_argument("-s", "--segLength",
            default=defaultSegLength,
            help="length of intervals for audio classification")

    showSegment = tasks.add_parser("showSegment",
            help="Read a videoFile and partition it in its show bpundaries")
    showSegment.add_argument("-i", "--inputFile",
            default=defaultVideoFile, help="Input File")
    showSegment.add_argument("-b", "--output",
            default=defaultBoundaryFile, help="File to output boundaries")
    showSegment.add_argument("-m", "--modelFile",
            default=defaultModel,
            help="classification model to be used for audio analysis")
    showSegment.add_argument("-td", "--templateDir",
            default=defaultTemplateDir, help="Directory containing templates")
    showSegment.add_argument("-st", "--subtitleFile",
            default=defaultSubtitleFile, help="subtitle file of input video")
    showSegment.add_argument("-si", "--skipInterval",
            default=defaultSkipIntervalsFile,
            help="File containing expected length of shows")
    showSegment.add_argument("-sd", "--outputDir",
            default=defaultSegmentationDir, help="save segmented video here")

    training    = tasks.add_parser("training",
            help="Train a custom music speech classification model")
    training.add_argument("-md", "--musicDir",
            default=defaultMusicDir, help="Directory containing music files")
    training.add_argument("-sd", "--speechDir",
            default=defaultSpeechDir, help="Directory containing speech files")
    training.add_argument("-mf", "--model",
            default=defaultOutputModelFile, help="Output Model")
    training.add_argument("-sr", "--samplingRate",
            default=defaultSamplingRate, help="sampling rate to be used")
    training.add_argument("-s", "--segLength",
            default=defaultSegLength,
            help="length of intervals for audio classification")

    showSegmentAnnotaions = tasks.add_parser("showSegmentAnnotated",
            help="Read an annotation file and segment video")
    showSegmentAnnotaions.add_argument("-i", "--inputFile",
            default=defaultVideoFile, help="video file")
    showSegmentAnnotaions.add_argument("-a", "--annotationsFile",
            default=defaultAnnotationFile, help="annotations file")
    showSegmentAnnotaions.add_argument("-si", "--startInd",
            default=defaultStartInd,
            help="Index of column containing start time")
    showSegmentAnnotaions.add_argument("-ei", "--endInd",
            default=defaultEndInd, help="Index of column containing end time")
    showSegmentAnnotaions.add_argument("-sdi", "--showDateInd",
            default=defaultShowDateInd,
            help="Index of column containing show date")
    showSegmentAnnotaions.add_argument("-sni", "--showNameInd",
            default=defaultShowNameInd,
            help="Index of column containing show name")
    showSegmentAnnotaions.add_argument("-pdi", "--pullDateInd",
            default=defaultPullDateInd,
            help="Index of column containing pull date")
    showSegmentAnnotaions.add_argument("-ci", "--channelInd",
            default=defaultChannelInd,
            help="Index of column containing end time")
    showSegmentAnnotaions.add_argument("-od", "--outputDir",
            default=defaultSegmentationDir, help="save segmented video here")

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    if (args.tasks == "showSegment"):
        showSegmentWrapper(args.inputFile, args.templateDir, args.modelFile,
                    args.skipInterval, args.subtitleFile, args.output,
                    args.outputDir)

    elif (args.tasks == "classification"):
        classificationWrapper(args.inputFile, args.outputFile, args.modelFile,
                    args.samplingRate, args.breakInterval, args.segLength)

    elif (args.tasks == "training"):
        trainingWrapper(args.musicDir, args.speechDir, args.model,
                    args.samplingRate, args.segLength)

    elif (args.tasks == "showSegmentAnnotated"):
        showSegmentFromAnnotationsWrapper(args.inputFile, args.annotationsFile,
                    args.startInd, args.endInd, args.showNameInd,
                    args.showDateInd, args.channelInd, args.pullDateInd,
                    args.outputDir)

    else:
        Error("Invalid Task")
