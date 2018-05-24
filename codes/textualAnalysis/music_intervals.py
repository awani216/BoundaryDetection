def musicarr (arr):
    i = 0
    res = []
    while(i<len(arr)):
        if arr[i]==1:
            j=i
            while arr[j]==1:
                j+=1
            if j-i >= 10:
                res.append([i,j])
            i = j
        else:
            i+=1
    return res

def do():
    fin = file('fin.txt')
    fop = open('res.txt', 'w')
    arr = []
    for line in fin:
        arr.append(int(float(line)))
    res = musicarr(arr)
    for i in range(len(res)):
        fop.write(str(res[i][0])+'-'+str(res[i][1])+'\n')
        print(res[i])
    fop.close()

do()
