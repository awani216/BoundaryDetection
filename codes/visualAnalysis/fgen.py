import os

def createFrames(dirname):
    if os.isdir(dirname):
        dirlist = os.listdir(dirname)
        dname = os.path.abspath("../../files_generated/audioAnalysis/music_intervals")
        relname = dirname.strip(dname)
        rootname =  r'/home/awanimishra/space/BoundaryDetection/files_generated/visualAnalysis/music_intervals'
        absname = rootname + relname
        os.makedirs(absname)
        for dirc in dirlist:
            if(dirc.endswith('.txt')):
                f.open((dirname + "/" + dirc),'r')
                for line in f:
                    basenm = os.path.splitext(dirc)[0]
                    videopath = os.path.abspath("../../../../Rosenthal/")
                    videopath = videopath + relname + "/" + dirc
                    end,start = line.split('-')
                    os.system("ffmpeg -ss " + start + " -i " + videopath + " -t " + start-end 
                    + " -vf fps=1 " + absname+"/"+basenm+ "%d.jpg")   
            elif os.isdir(dirname + '/' + dirc):
                createFrames(dirname + '/' + dirc)
       

createFrames(os.path.abspath("../../files_generated/music_intervals"))