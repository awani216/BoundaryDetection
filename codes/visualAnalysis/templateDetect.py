#template detection for identifying logos

import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
from multiprocessing import Pool, cpu_count


def prog_len(i, skipIntervals):
    i = i.split("/")[-1]
    a = [x for x in skipIntervals if x[0] in i]
    if (a == []):
        return -1
    return int(a[0][1])

#print(w,h)

def sqdiff_normed(imageA, imageB):
    errp = 1000
    for i in range(3):
        err = np.sum(np.square(imageA[:,:,i].astype("float") - imageB[:,:,i].astype("float")))
        var = np.sum(np.square(imageA[:,:,i].astype("float")) *  np.sum(np.square(imageB[:,:,i].astype("float"))))
        std = np.sqrt(var)
        err /= std
        errp = errp * err
    return errp

def ccorr_normed(imageA, imageB):
        errp = 1
        for i in range(3):
            corr = np.corrcoef(imageA[:,:,i].flatten(), imageB[:,:,i].flatten())[0][1]
            errp = errp * corr
        return errp

def sqdiff_wrapper(args):
    return sqdiff_normed(*args)

def find(ip, start, templates):
    i = -1
    for template in templates:
        i+=1
        res = ccorr_normed(ip, template)
        threshold = 0.44
        loc = (res>threshold)
        if (loc):
            return (True, i)
    return (False, 0)

def findFrames(videoFile, templateDir, intervalFile, musicSpeechFile, matchedFramesDir, outputFile):
    cap = cv2.VideoCapture(videoFile)

    w  = int(cap.get(3))
    h  = int(cap.get(4))

    templates = []
    template_files = os.listdir(templateDir)
    for t_file in template_files:
        template1 = cv2.imread(templateDir + "/" +  t_file,-1)
        template = cv2.resize(template1, (w,h))
        templates.append(template)
        print(template.shape)

    skipIntervals = []
    intervals     = open(intervalFile, 'r')
    for line in intervals:
        name, interval = line.split(":")
        skipIntervals.append([name, interval])

    fps = cap.get(5)
    print(fps)
    f = open(musicSpeechFile, 'r')
    musicIntervals = []
    for line in f:
        a, b = line.split("-")
        a, b = int(a), int(b)
        musicIntervals.append([a,b])
    n = len(musicIntervals)
    curr = 0
    matches = []
    while(curr<n):
        i, j = musicIntervals[curr][0] -2, musicIntervals[curr][1]+2
        start = int(i*fps)
        end   = int(j*fps)
        cap.set(1, start)
        curr += 1;
        while(start<=end):
            ret, frame = cap.read()
            if(not ret):
                break
            succ, prog = find(frame, start, templates)
            if(succ):
                print(start/fps, template_files[prog])
                matches.append(str(start/fps) + ":" + template_files[prog].split(".")[0])
                cv2.imwrite(matchedFramesDir + "/" + str(start/fps) + ".png", frame)
                skip_len = prog_len(template_files[prog], skipIntervals)
                if(skip_len > 100):
                    i += skip_len - 100
                    while (musicIntervals[curr+1][0]<i and curr<n):
                        curr += 1
                break
            skipFrames = 4
            while(skipFrames):
                skipFrames -= 1
                cap.read()
            start += 5
    f = open(outputFile, 'w')
    for i in matches:
        f.write(i +  '\n')
    f.close()


#findFrames("v.mp4", "template", "skipIntervals.txt", "commercial_removed.txt", "./", "boundaries.txt")
