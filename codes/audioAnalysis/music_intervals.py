#identification of music intervals and music-speech intervals

import re 
import sys  
import os

reload(sys)  
sys.setdefaultencoding('utf8')

def find_captions():
    
        if file.endswith('.txt3'):
            datafile = file
            f = open(r'/home/walter-white/Desktop/test/files_generated/audioAnalysis/music_intervals.txt','w')
            s = open(r'/home/walter-white/Desktop/test/files_generated/audioAnalysis/music_speech_intervals.txt','w') 
            #r = open(r'/home/walter-white/Desktop/test/files_generated/audioAnalysis/speech_intervals.txt','w') 
            found = 0
            found1 = 0
            #found2 = 0
            music = u'\u266A\u266A'
            music_speech = u'\u266A'
            print(music)
            for line in datafile:
                line = line.decode('utf-8')
                if re.search(music,line) : 
                    found = found + 1
                    time = str(3600*int(line[8:10])+60*int(line[10:12])+1*int(line[12:14])+10)+'-'+str(3600*int(line[27:29])+60*int(line[29:31])+int(line[31:33])-10)
                    f.write(time+'\n')
                    print(line)
                    print(time)
                elif re.search(music_speech,line) :
                    found1 = found1 + 1
                    time = str(3600*int(line[8:10])+60*int(line[10:12])+1*int(line[12:14])+10)+'-'+str(3600*int(line[27:29])+60*int(line[29:31])+int(line[31:33])-10)
                    s.write(time+'\n')
                    print(line)
                    print(time) 

            
            print(found)
            print(found1)
            print(found + found1)
            f.close()
            return found+found1 
def findAllExtfiles(dirname):
    if os.path.isdir(dirname) :
        dirlist = os.listdir(dirname)
        #print(dirlist)
        for name in dirlist:
            if(name.enddswith('.txt3') or name.endswith('.txt')):
                print(name)
            elif(name.find(".") == -1):
                findAllExtfiles(dirname + "/" + name)


findAllExtfiles(os.path.abspath("../../../../Rosenthal"))
#print find_captions()
