def musicIntervalsArray (arr):
    i = 0
    res = []
    while(i<len(arr)):
        if arr[i]==1:
            j=i
            while j<len(arr) and arr[j]==1:
                j+=1
            if j-i >= 3:
                res.append([i,j])
            i = j
        else:
            i+=1
    return res

def makeMusicSpeechIntervals(audioClassificationFile, audioSpeechIntervalFile):
    fin = open(audioClassificationFile, 'r')
    fop = open(audioSpeechIntervalFile, 'w')
    arr = []
    for line in fin:
        arr.append(int(float(line)))
    res=musicIntervalsArray(arr)
    count = 0
    for i in range(len(res)):
        count = count + res[i][1] - res[i][0]
        fop.write(str(res[i][0])+'-'+str(res[i][1])+'\n')

    print(count)
    fop.close()

#makeMusicSpeechIntervals()
