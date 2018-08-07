#template detection for identifying logos

import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

templates = []
template_files = os.listdir("template")

def prog_len(i):
    if (i >= 1 and i<= 5):
        return 3600
    else:
        return 1800
    
cap = cv2.VideoCapture("v2.mp4")

w  = int(cap.get(3))
h  = int(cap.get(4))
#print(w,h)

def mse(imageA, imageB):
    err = np.sum(np.square(imageA.astype("float") - imageB.astype("float")))
    var = np.sum(np.square(imageA.astype("float")) *  np.sum(np.square(imageB.astype("float")**2)))
    std = np.sqrt(var)
    err /= std
                            
    return err

for t_file in template_files:
    template1 = cv2.imread("template/" +  t_file,-1)
    template = cv2.cvtColor(template1, cv2.COLOR_BGR2GRAY)
    template = cv2.resize(template, (w,h))
    templates.append(template) 
    print(template.shape)

def find(ip, start):
    img_gray = cv2.cvtColor(ip, cv2.COLOR_BGR2GRAY)
    i = 0
    for template in templates:
        i += 1
        w, h = template.shape[::-1]
        res = mse(img_gray,template)
        threshold = 0.0004
        loc =  (res <= threshold)
        if (loc):
            cv2.imwrite("img" +  str(start) + ".png", img_gray)
            return (True, (prog_len(i)))
    return (False, 0)


import time
i=1
fps = cap.get(5)
startTime = time.time()

f = open("commercial_removed.txt", 'r')

for line in f:
    i, j = line.split("-")
    i, j = int(i)-2, int(j)+2
    start = int(i*fps)
    end   = int(j*fps)
    cap.set(1, start)
    while(start<=end):
        ret, frame = cap.read()
        succ, skip_len = find(frame, start)
        if(succ):
            print(start/fps)
        skipFrames = 9
        while(skipFrames):
            skipFrames -= 1
            cap.read()
        start += 10
print(time.time()-startTime)



