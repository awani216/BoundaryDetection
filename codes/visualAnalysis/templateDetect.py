#template detection for identifying logos

import cv2
import numpy as np
from matplotlib import pyplot as plt
import os


def prog_len(i, skipIntervals):
    i = i.split("/")[-1]
    a = [x for x in skipIntervals if x[0] in i]
    if (a == []):
        return -1
    return a[0][1]

#print(w,h)

def sqdiff_normed(imageA, imageB):
    err = np.sum(np.square(imageA.astype("float") - imageB.astype("float")))
    var = np.sum(np.square(imageA.astype("float")) *  np.sum(np.square(imageB.astype("float")**2)))
    std = np.sqrt(var)
    err /= std

    return err


def find(ip, start, templates):
    img_gray = cv2.cvtColor(ip, cv2.COLOR_BGR2GRAY)
    i = 0
    for template in templates:
        i += 1
        w, h = template.shape[::-1]
        res = sqdiff_normed(img_gray,template)
        threshold = 0.0004
        loc =  (res <= threshold)
        if (loc):
            cv2.imwrite("img" +  str(start) + ".png", img_gray)
            return (True, i-1)
    return (False, 0)

def findFrames(videoFile, templateDir, intervalFile, musicSpeechFile):
    cap = cv2.VideoCapture(videoFile)

    w  = int(cap.get(3))
    h  = int(cap.get(4))

    templates = []
    template_files = os.listdir(templateDir)
    for t_file in template_files:
        template1 = cv2.imread(templateDir + "/" +  t_file,-1)
        template = cv2.cvtColor(template1, cv2.COLOR_BGR2GRAY)
        template = cv2.resize(template, (w,h))
        templates.append(template)
        print(template.shape)
        
    skipIntervals = []
    intervals     = open(intervalFile, 'r')
    for line in intervals:
        name, interval = line.split(":")
        skipIntervals.append([name, interval])

    fps = cap.get(5)

    f = open(musicSpeechFile, 'r')
    musicIntervals = []
    for line in f:
        a, b = line.split("-")
        a, b = int(a), int(b)
        musicIntervals.append([a,b])
    n = len(musicIntervals)
    curr = 0
    while(curr<n):
        i, j = musicIntervals[curr][0] -2, musicIntervals[curr][1]+2
        start = int(i*fps)
        end   = int(j*fps)
        cap.set(1, start)
        curr += 1;
        while(start<=end):
            ret, frame = cap.read()
            succ, prog = find(frame, start, templates)
            if(succ):
                print(start/fps, template_files[prog])
                skip_len = prog_len(template_files[prog], skipIntervals)
                if(skip_len > 100):
                    i += skip_len - 100
                    while (musicIntervals[curr+1, 0]<i and curr<n):
                        curr += 1
                break
            skipFrames = 9
            while(skipFrames):
                skipFrames -= 1
                cap.read()
            start += 10



findFrames("v2.mp4", "template", "skipIntervals.txt", "commercial_removed.txt")
