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

#iterating over the rows and checking if the videofilepath corresponding to manual annotation is given
for i in f1:
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
    #Checking if audio hint is present or not
    if(i[17]=='y' or i[17]=='Y'):
        #multiple intervals were present hence we need to extract audio from every intervals
        intervals = i[19].split(",")
        #iterating over every interval 
        for interval in intervals :
            h, m, s = (interval.split("-")[0]).split(':')
            time = str(int(h)*3600+int(m)*60+int(s))
            #if end time if not given then we extracted the 5 sec audio 
            duration = "5"
            if (len(interval.split("-")) >= 2):
                h1, m1, s1 = interval.split("-")[1].split(":")
                #value of duration has been changed since the end time was given
                duration = str(int(h1)*3600 + int(m1)*60 + int(s1) - time)
            os.system("ffmpeg -i " + videofilepath + " -ss "+ time +" -t " 
                    + duration + " -q:a 0 -map a " + path + dir3 + "-" 
                    + h.strip() + "-" + m.strip() + "-" + s.strip() + ".mp3")
    else:
        #if no audio hint was present we simply extracted a 5 sec audion from start of the show
        #these are stored inside a folder named nomusic 
        intervals = i[7]
        for interval in intervals :
            h, m, s = (interval.split("-")[0]).split(':')
            time = str(int(h)*3600+int(m)*60+int(s)-2) 
            duration = "5"
            if (len(interval.split("-")) >= 2):
                h1, m1, s1 = interval.split("-")[1].split(":")
                duration = str(int(h1)*3600 + int(m1)*60 + int(s1) - time)
            os.system("ffmpeg -i " + videofilepath + " -ss "+ time +" -t " 
                    + duration + " -q:a 0 -map a " + path + "nomusic/" + dir3 + "-" 
                    + h.strip() + "-" + m.strip() + "-" + s.strip() + ".mp3")
    
