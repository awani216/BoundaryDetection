###############################################################################
#------------------Template Detection Module----------------------------------#
# Author: Awani Mishra                                                        #
# Task  : Find show boundaries using templates provided                       #
#-----------------------------------------------------------------------------#

import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
from multiprocessing import Pool, cpu_count

## Search in the file skipIntervals and find the length of the show.
# Definition of parameters
# fileName      : The name of template file which is matched  in the video
# skipIntervals : Array of ShowName/Intervals pair used to detect template.
# Output
# Length of the show which is detected. If show is not in the file, return -1
def prog_len(fileName, skipIntervals):
    i = fileName.split("/")[-1]
    a = [x for x in skipIntervals if x[0] in i]
    if (a == []):
        return -1
    return int(a[0][1])

## Suare Difference Normed evaluation metric for two images. It is sum of differences
# squared between the input images divided by their variances.
# Definition of parameters:
# imageA, imageB :  the two images whose similarity is to be computed
# Output : sqdiff_normed metric [The smaller the value, the closer the images]
def sqdiff_normed(imageA, imageB):
    errp = 1000
    for i in range(3):
        err = np.sum(np.square(imageA[:,:,i].astype("float") - imageB[:,:,i].astype("float")))
        var = np.sum(np.square(imageA[:,:,i].astype("float")) *  np.sum(np.square(imageB[:,:,i].astype("float"))))
        std = np.sqrt(var)
        err /= std
        errp = errp * err
    return errp


## Correlation Normed evaluation metric for two images. It is sum of differences
# squared between the input images divided by their variances.
# Definition of parameters:
# imageA, imageB :  the two images whose similarity is to be computed
# Output : ccorr_normed metric [The larger the value, the closer the images]
def ccorr_normed(imageA, imageB):
        errp = 1
        for i in range(3):
            corr = np.corrcoef(imageA[:,:,i].flatten(), imageB[:,:,i].flatten())[0][1]
            errp = errp * corr
        return errp

## Check if the input frame matches a template
# Definition of parameters:
# ip: input frame
# templates : Array of templates to be used for matching
# Output: Returns a pair(Bool, int). If image is matched,
# returns (True, index of template matched), otherwise (False, 0)
def find(ip, templates):
    i = -1
    for template in templates:
        i+=1
        # Using ccorr_normed metric for similarity.
        res = ccorr_normed(ip, template)
        # threshold based on experimentation. Can be chenged based on requirment
        threshold = 0.44
        loc = (res>threshold)
        if (loc):
            return (True, i)
    return (False, 0)

## Main function to check for templates in intetvals specified by user.
## Defining variales
# videoFile   : videoFile to detect frames in.
# templateDir : directory that contains templates. Please name the template as <showname>i.mp4
#               where i can be used to separate two templates of same show.
# skipIntervalFile : File containing showName and its expected duration. The show name should be consistent
#                    with the showname used in template files.
# searchIntervals  : intervals to search the file in. This could be based on audioAnalysis or
#                    on the basis of captions.
# matchedFramesDir : Directory where matched frames will be saved.
# outputFile       : A file where matches will be saved in <seconds from start> <showname> format
#                    for example, if Ellen is found after 50 secs, it will be saved as "50 Ellen"
def findFrames(videoFile, templateDir, skipIntervalFile, searchIntervalFile, matchedFramesDir, outputFile):
    # loading the video into opencv VideoCapture
    cap = cv2.VideoCapture(videoFile)

    # Getting frame height and width
    w  = int(cap.get(3))
    h  = int(cap.get(4))

    # Loading templates and resizing them to match the frames of video
    templates = []
    template_files = os.listdir(templateDir)
    for t_file in template_files:
        template1 = cv2.imread(templateDir + "/" +  t_file,-1)
        template = cv2.resize(template1, (w,h))
        templates.append(template)
        print(template.shape)

    # Loading skip intervals in specified format.
    skipIntervals = []
    intervals     = open(skipIntervalFile, 'r')
    for line in intervals:
        name, interval = line.split(":")
        skipIntervals.append([name, interval])

    fps = cap.get(5)

    # Getting intervals to search in the video
    f = open(searchIntervalFile, 'r')
    searchIntervals = []
    for line in f:
        a, b = line.split("-")
        a, b = int(a), int(b)
        searchIntervals.append([a,b])

    # Beginning with frame detection
    n = len(searchIntervals)
    curr = 0
    matches = []
    while(curr<n):
        i, j = searchIntervals[curr][0] -2, searchIntervals[curr][1]+2
        start = int(i*fps)
        end   = int(j*fps)
        cap.set(1, start)
        curr += 1;
        while(start<=end):
            ret, frame = cap.read()
            if(not ret):
                break
            succ, prog = find(frame, templates)
            ## Video is matched, so we save the image and jump by the skip Interval.
            if(succ):
                print(start/fps, template_files[prog])
                matches.append(str(start/fps) + ":" + template_files[prog].split(".")[0])
                cv2.imwrite(matchedFramesDir + "/" + str(start/fps) + ".png", frame)
                skip_len = prog_len(template_files[prog], skipIntervals)
                if(skip_len > 100):
                    i += skip_len - 100
                    while (searchIntervals[curr+1][0]<i and curr<n-1):
                        curr += 1
                break
            #skipping 4 frames i.e. appx 0.2 seconds
            skipFrames = 4
            while(skipFrames):
                skipFrames -= 1
                cap.read()
            start += 5

    # Saving the results
    f = open(outputFile, 'w')
    for i in matches:
        f.write(i +  '\n')
    f.close()
    return matches


#findFrames("v.mp4", "template", "skipIntervals.txt", "commercial_removed.txt", "./", "boundaries.txt")
