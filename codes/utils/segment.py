###############################################################################
#------------------Segmentation Module----------------------------------------#
# Author: Awani Mishra                                                        #
# Task  : Segment the video file on the basis of input                        #
#-----------------------------------------------------------------------------#

import os
import time
import csv

def get_sec(time_str):
    # get seconds from hh:mm:ss string
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s.split(".")[0])

## Use generated output to create segments
## Files are named YYYY-MM-DD_HH_MM_SS_ShowName.mp4 (Here date is show date and time is start time)
## Definition of parameters
# showDate  : Date on which show is recorded
# matches   : 2D Array containing results in format [time, showName]
# videoFile : path to videoFile
# outputDir : directory to output videos
# Output
# Creates segments in the format <showDate>_<showTime>_<showName>.mp4
def segmentUsingSegmenetationResults(showDate, matches, videoFile, outputDir):

    # Creating boundaries for first n-1 shows using pescribed format
    n = len(matches)
    for i in range(n-1):
        showTime = "_".join(time.strftime('%H:%M:%S', time.gmtime(int(matches[i][0]))).split(":"))
        showName = matches[i][1]
        outputFile = outputDir + "/" + showDate + "_" + showTime + "_" + showName + ".mp4"
        startTime = str(matches[i][0] - 60)
        duration  = str(matches[i+1][0] - matches[i][0] + 120)
        command = "ffmpeg -i " +  videoFile + " -ss " + startTime + " -t " + duration + " -c copy " + outputFile
        os.system(command)

    # Creating last boundary
    showTime = "_".join(time.strftime('%H:%M:%S', time.gmtime(int(matches[n-1][0]))).split(":"))
    showName = matches[n-1][1]
    outputFile = outputDir + "/" + showDate + "_" + showTime + "_" + showName + ".mp4"
    startTime = str(matches[n-1][0] - 60)
    command = "ffmpeg -i " +  videoFile + " -ss " + startTime + " -c copy " + outputFile
    os.system(command)

## Reads into an annotation file and segments video based on this file
## Files are named YYYY-MM-DD_HH_MM_SS_ShowName.mp4 (Here date is show date and time is start time)
## Definition of parameters (Indexes should be 0 indexed i.e. [0,1,2..] instead of [1,2,3..])
# videoFile      : path to videoFile. Video should be named YYYY-MM-DD*.mp4 where the date is its pulldate
# annotationFile : path to annotationFile
# startInd       : index of column containing starting Time
# endInd         : index of column containing ending Time
# showNameInd    : index of column containing show name
# showDateInd    : index of column containing show date [YYYY-MM-DD format]
# channelInd     : index of file containing channelName
# pullDateInd    : index of column containing pull date [YYYY-MM-DD format]
# outputDir      : directory to extract videoFile
# Output
# Creates segments in the format <channelName>_<showDate>_<showTime>_<showName>.mp4
def segmentUsingAnnotations(videoFile, annotationFile, startInd, endInd,
showNameInd, showDateInd, channelInd, pullDateInd, outputDir):
    annotation = open(annotationFile, 'r')
    annotation = csv.reader(annotation)

    for line in annotation:
        ## Checking if the video pull date and the video matches, to avoid errors
        #  in files which have annotaions for more than 1 video.
        pulldate      = line[pullDateInd]
        videoPullDate = "-".join([videoFile[0:4], videoFile[5:7], videoFile[8:10]])
        if(pulldate  != videoPullDate):
            continue
        showDate      = line[showDateInd]
        showTime      = "-".join(line[startInd].split(":"))
        print(pulldate)
        startTime     = get_sec(line[startInd])
        endTime       = get_sec(line[endInd])
        duration      = endTime - startTime
        showName      = line[showNameInd]
        channelName   = line[channelInd]
        outputFile = outputDir + "/" + channelName + "_" + showDate + "_" + showTime + "_" + showName + ".mp4"
        command = "ffmpeg -i " +  videoFile + " -ss " + str(startTime) + " -t " + str(duration)  + " -c copy " + outputFile
        print(command)
        os.system(command)
