###############################################################################
#------------------Date and Time Utilities---------------------------------------------#
# Author: Awani Mishra                                                        #
# Task  : Utilities for manipulating date and time                            #
#-----------------------------------------------------------------------------#

# TODO: Move various date and time functions scattered throughout to this central module

from datetime import date, timedelta


# Find out the show date from the pull date. The assumption is that pullDay is
# one working day ahead of the showDay. Hence, show pulled on tuesday was from
# monday and on monday was from friday.
#
# Definition of parameters
# videoFile : name of video file in the format YYYY-MM-DD*.mp4.
# Output is a date string in the format YYYY-MM-DD
def findShowDate(videoFile):
    videoFile = videoFile.split("/")[-1]
    year  = int(videoFile[0:4])
    month = int(videoFile[5:7])
    day   = int(videoFile[8:10])
    pullDate = date(year, month, day)
    pullDay  = pullDate.weekday()
    # 0 implies day is monday, so we shift back 3 days.
    if(pullDay == 0):
        showDate = pullDate -  timedelta(days=3)
    else:
        showDate = pullDate -  timedelta(days=1)
    return showDate
