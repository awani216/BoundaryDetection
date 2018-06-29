#code for extracting the music samples
import os
import glob
import csv
#filename -> annotation file corresponding to video used for data extraction
#path -> where the data will be saved
#videofilepath -> path to video used for data extraction

filepath = "datafile.csv" 
path = "musicext/"
videofilepath = "" 

f1 = open(filepath,'r')
f1 = csv.reader(f1)
for i in f1:
    if(i[15]=='y' or i[15]=='Y'):
        pulldate = i[2]
        vtype = "V" + i[1].strip().split(".")[0]
        #month, day, year = pulldate.split("/")
        year,month,day = pulldate.split("-")
        dir1 = year
        dir2 = dir1 + "-" + month
        dir3 = dir2 + "-" + day
        rootdir = "/mnt/netapp/NewsScape/Rosenthal/"
        folderpath = rootdir + dir1 + "/" + dir2 + "/" + dir3 + "/"
        folderpath = ""
        wildstring = folderpath + dir3 + "*" + vtype + "*" + ".mp4"
        print(wildstring)
        if (glob.glob(wildstring) == []):
            continue
        videofilename = glob.glob(wildstring)[0]
        intervals = i[17].split(",")
        for interval in intervals :
            h, m, s = (interval.split("-")[0]).split(':')
            time = str(int(h)*3600+int(m)*60+int(s)) 
            os.system("ffmpeg -i " + videofilename + " -ss "+ time +" -t 5 -q:a 0 -map a " 
                    + path + dir3 + "-" + h.strip() + "-" + m.strip() + "-" + s.strip() + ".mp3")
