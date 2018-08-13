import numpy as np
import os

def remove_commercials(commercialsFile, musicFile, outputFile ):
    commercials_file = open(commercialsFile, 'r')
    music_file = open(musicFile, 'r')

    commercial_intervals = []

    for line in commercials_file:
        i,j = line.split("-")
        commercial_intervals.append(([int(i),int(j)]))

    music_intervals = []

    for line in music_file:
        i,j = line.split("-")
        music_intervals.append([int(i),int(j)])

    dlist = []
    for i in range(len(music_intervals)):
        music_start = music_intervals[i][0]
        music_end   = music_intervals[i][1]
        for j in range(len(commercial_intervals)):
            com_start = commercial_intervals[j][0]
            com_end   = commercial_intervals[j][1]
            if (music_start>=com_start and music_end<=com_end):
                dlist.append(i)
            elif (music_start>=com_start and music_start<=com_end):
                music_intervals[i][0] = com_end
            elif (music_end>=com_start and music_end<=com_end):
                music_intervals[i][1] = com_start
    print(np.array(music_intervals))

    music_intervals = list(np.delete(np.array(music_intervals), dlist, axis=0))
    print(music_intervals)
    f = open(outputFile, 'w')
    count = 0
    for i in music_intervals:
        count = count + i[1] - i[0]
        line = str(i[0]) + "-" + str(i[1]) + "\n"
        f.write(line)

    print(count)
