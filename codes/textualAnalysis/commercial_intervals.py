###############################################################################
#------------------Commercial Intervals Module--------------------------------#
# Author: Awani Mishra                                                        #
# Task  : Search for commercial intervals in the module                       #
#-----------------------------------------------------------------------------#

import re

## Given a subtitle file, return commercial intervals
# We assume that the Subtitle lists time in the format:
# YYYYMMDDHHMMSS|YYYYMMDDHHMMSS (Year-Month-Day-Hours-Minutes-Seconds)
# Definition of parameters
# subtitleFile : Subtitle file
# outputFile   : File to output results
# Output format : List of intervals in the format start-end (in seconds) 
def find_commercials(subtitleFile, outputFile):
        datafile = open(subtitleFile, 'r')
        f = open(outputFile,'w')
        found = 0
        # Regular expression to find the string "Type=Commercial". Replace with
        # whatever commercial identifier your file has.
        ignorecase = re.compile('Type=Commercial', re.IGNORECASE)
        for line in datafile:
            if ignorecase.search(line) :
                found = found + 1
                # If the time is not listed in the above format, change this portion of code.
                time = str(3600*int(line[8:10])+60*int(line[10:12])+1*int(line[12:14])+10)+'-'+str(3600*int(line[27:29])+60*int(line[29:31])+int(line[31:33])-10)
                f.write(time+'\n')
                print(line)
                print(time)


        f.close()
        return found


#print find_commercials(subtitleFile, outputFile)
