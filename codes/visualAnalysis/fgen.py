import subprocess
import os

def createFrames(dirname):
    if os.isdir(dirname):
        dirlist = os.listdir(dirname)
        dname = os.path.abspath("../../files_generated/music_intervals")
        relname = dirlist.strip(dname)
        rootname =  r'/home/awanimishra/space/BoundaryDetection/files_generated/visualAnalysis/music_intervals'
        absname = rootname + relname
        os.makedirs(absname)
        rootname =  r'/home/awanimishra/space/BoundaryDetection/files_generated/visualAnalysis/music_speech_intervals'
        absname = rootname + relname
        os.makedirs(absname)
        for dir in dirlist:
            if(dir.endswith('.txt')):
                subprocess.call(['./frames.sh'])
            elif os.isdir(dir)
                createFrames(dir)


createFrames(os.path.abspath("../../files_generated/music_intervals"))