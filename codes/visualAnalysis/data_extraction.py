#code for extracting the music samples
import os
import glob
import csv
#filename -> annotation file corresponding to video used for data extraction
#path -> where the data will be saved
#videofilepath -> path to video used for data extraction

filepath = "../../files_used/audioAnalysis/datafile_V12 Skylar.csv"
path = "../../files_generated/visualAnalysis/imageext/V12/"
videofilename = "2006-01-10_0000_US_00001670_V12_VHS4_MB1_E1_JN.mp4"
path1 = "../../files_generated/visualAnalysis/imageext/noimage/V12/"

f1 = open(filepath,'r')
f1 = csv.reader(f1)

#iterating over the rows and checking if the file path corresponding to manual annotation is given
for i in f1:
    pulldate = i[2].split(" ")[0]
    vtype = "V" + i[1].strip().split(".")[0]
    if(len(pulldate.split("/")) == 3):
        month, day, year = pulldate.split("/")
    elif (len(pulldate.split("-"))==3):
        year,month,day = pulldate.split("-")
    else:
        continue
    dir1 = year
    dir2 = dir1 + "-" + month
    dir3 = dir2 + "-" + day
    rootdir = "/mnt/netapp/NewsScape/Rosenthal/"
    folderpath = rootdir + dir1 + "/" + dir2 + "/" + dir3 + "/"
    videofilepath = folderpath + videofilename
    # Check if the file exixts.
    if (not os.path.exists(videofilepath)):
        print("video file not found")
        continue
    #Checking if pictorial hint is present or not
    if((i[14]=='y' or i[14]=='Y') and (i[16])):
        intervals = i[16].split(", ")
        for interval in intervals :
            print(interval)
            h, m, s = (interval.split("-")[0]).split(':')
            print(h + " " + m + " " + s)
            time = str(int(h)*3600+int(m)*60+int(s))
            duration = "5"
            destpath = path + dir3 + "-" + vtype + "-" + h.strip() + "-" + m.strip() + "-" + s.strip() + ".mp3"
            if os.path.exists(destpath):
                os.remove(destpath)
            if (len(interval.split("-")) >= 2):
                print(interval.split("-")[1].split(":"))
                h1, m1, s1 = interval.split("-")[1].split(":")
                print(h1+" "+m1+" "+s1)
                duration = str(int(h1)*3600 + int(m1)*60 + int(s1) - int(time))
            os.system("ffmpeg -ss " + time + " -i " + videofilepath + " -t " + duration 
                    + " -vf fps=1 " + destpath + "%d.jpg")       
    else:
        intervals = i[8].split(",")
        for interval in intervals :
            h, m, s = (interval.split("-")[0]).split(':')
            time = str(int(h)*3600+int(m)*60+int(s)-2)
            duration = "5"
            destpath = path1 + dir3 + "-" + vtype + "-" + h.strip() + "-" + m.strip() + "-" + s.strip() + ".mp3"
            if os.path.exists(destpath):
                os.remove(destpath)

            if (len(interval.split("-")) >= 2):
                h1, m1, s1 = interval.split("-")[1].split(":")
                duration = str(int(h1)*3600 + int(m1)*60 + int(s1) - time)
            os.system("ffmpeg -ss " + time + " -i " + videofilepath + " -t " + duration 
            + " -vf fps=1 " + destpath + "%d.jpg")       

