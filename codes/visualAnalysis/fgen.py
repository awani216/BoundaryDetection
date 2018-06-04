import os

def createFrames(dirname):
    if os.isdir(dirname):
        dirlist = os.listdir(dirname)
        dname = os.path.abspath("../../files_generated/audioAnalysis/music_intervals")
        relname = dirlist.strip(dname)
        rootname =  r'/home/awanimishra/space/BoundaryDetection/files_generated/visualAnalysis/music_intervals'
        absname = rootname + relname
        os.makedirs(absname)
        for dirc in dirlist:
            if(dirc.endswith('.txt')):
                f.open((dirname + "/" + dirc),'r')
                for line in f:
                    videopath = os.path.abspath("../../../../Rosenthal/")
                    videopath = videopath + relname.strip(".txt") + ".mp4"
                    end,start = line.split('-')
                    os.system("ffmpeg -ss " + start + " -i " + videopath + " -t " + start-end + " -vf fps=1 " + absname+"/"+dirc.strip(".txt")+ "%d.jpg")   
            elif os.isdir(dirc)
                createFrames(dirname + '/' + dirc)
       

createFrames(os.path.abspath("../../files_generated/music_intervals"))