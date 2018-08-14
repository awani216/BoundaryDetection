###############################################################################
#------------------Commercial Removal Module----------------------------------#
# Author: Awani Mishra                                                        #
# Task  : Remove commercial intervals from any interval file                  #
#-----------------------------------------------------------------------------#

import numpy as np
import os

def remove_commercials(commercialsFile, intervalFile, outputFile ):
    commercials_file = open(commercialsFile, 'r')
    interval_file    = open(intervalFile, 'r')

    commercial_intervals = []

    for line in commercials_file:
        i,j = line.split("-")
        commercial_intervals.append(([int(i),int(j)]))

    intervals = []

    for line in interval_file:
        i,j = line.split("-")
        intervals.append([int(i),int(j)])

    dlist = []
    for i in range(len(intervals)):
        start = intervals[i][0]
        end   = intervals[i][1]
        for j in range(len(commercial_intervals)):
            com_start = commercial_intervals[j][0]
            com_end   = commercial_intervals[j][1]
            if (start>=com_start and end<=com_end):
                dlist.append(i)
            elif (start>=com_start and start<=com_end):
                intervals[i][0] = com_end
            elif (end>=com_start and end<=com_end):
                intervals[i][1] = com_start

    intervals = list(np.delete(np.array(intervals), dlist, axis=0))
    f = open(outputFile, 'w')
    count = 0
    for i in intervals:
        count = count + i[1] - i[0]
        line = str(i[0]) + "-" + str(i[1]) + "\n"
        f.write(line)

    print(count)
