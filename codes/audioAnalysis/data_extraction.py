#code for extracting the music samples
import os
import glob
import csv
#filename -> annotation file corresponding to video used for data extraction
#path -> where the data will be saved
#videofilepath -> path to video used for data extraction

filepath = "datafile.csv" 
path = "musicext/"
videofilename = "" 

f1 = open(filepath,'r')
f1 = csv.reader(f1)
for i in f1:
    if(i[17]=='y' or i[17]=='Y'):
        pulldate = i[2].split(" ")[0]
        vtype = "V" + i[1].strip().split(".")[0]
        if(len(pulldate.split("/")) == 3): 
            month, day, year = pulldate.split("/")
        else:
            year,month,day = pulldate.split("-")
        dir1 = year
        dir2 = dir1 + "-" + month
        dir3 = dir2 + "-" + day
        rootdir = "/mnt/netapp/NewsScape/Rosenthal/"
        folderpath = rootdir + dir1 + "/" + dir2 + "/" + dir3 + "/"
        videofilepath = folderpath + videofilename
        # Check if the file exixts.
        if (not os.path.exists(videofilepath)):
            continue
        intervals = i[19].split(",")
        for interval in intervals :
            h, m, s = (interval.split("-")[0]).split(':')
            time = str(int(h)*3600+int(m)*60+int(s)) 
            duration = "5"
            if (len(interval.split("-")) >= 2):
                h1, m1, s1 = interval.split("-")[1].split(":")
                duration = str(int(h1)*3600 + int(m1)*60 + int(s1) - time)
            os.system("ffmpeg -i " + videofilepath + " -ss "+ time +" -t " 
                    + duration + " -q:a 0 -map a " + path + dir3 + "-" 
                    + h.strip() + "-" + m.strip() + "-" + s.strip() + ".mp3")
