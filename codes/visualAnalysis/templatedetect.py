import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

def find(ip, template_files):
    img_rgb = cv2.imread(ip, -1)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    for template in template_files:
        template1 = cv2.imread("template/" +  template,-1)
        template = cv2.cvtColor(template1, cv2.COLOR_BGR2GRAY)

        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
#    print(res)
        loc = np.where( res >= threshold)
       # print(len(loc))
        #if(len(loc) is not 0):
           # print(ip.split("/")[1])
        k = 0
        for pt in zip(*loc[::-1]):
            if(k==0):
                k=1
                print(ip.split("/")[1])

            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    cv2.imwrite("ellen2/"+ip.split("/")[1],img_rgb)

image_files = os.listdir("generated2")
template_files = os.listdir("template")
for image in image_files:
    ip = "generated2/"+image
    find(ip, template_files)
