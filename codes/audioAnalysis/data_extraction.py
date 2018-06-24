#code for extracting the music samples
import os

#filename -> annotation file corresponding to video used for data extraction
#path -> where the data will be saved
#videofilepath -> path to video used for data extraction

filepath = 
path = 
videofilepath = 

f1 = open(filepath,'r')
for i in f1:
    if(f1[i][10]=='y' or f1[i][10]=='Y'):
        h, m, s = (f1[i][12]).split(':')
        time = str(int(h)*3600+int(m)*60+int(s)) 
        os.sysem("ffmpeg -i " + videofilepath + " -ss "+ time +" -t 5 -q:a 0 -map a " + path)
