import numpy as np

file = open('ans.txt')

sp = []
d = []

for line in file:
    temp =  line.split('-')
    sp.append([int(temp[0]), int(temp[1])])

for i in range(len(sp)):
    j=i
    if(i+1<len(sp)):
        while i+1 < len(sp) and sp[i+1][0]-sp[i][1]<=96:
            i = i+1
            d.append(i)
        sp[j][1]=sp[i][0]

ans = np.delete(sp, d, 0)

f = open(r'/file_generated/combine_speech.txt','w')
for i in range(len(ans)):
    text = str(ans[i][0]) +'-'+str(ans[i][1])
    f.write(text+'\n')

f.close()


print(' start         end')
f.close()

for i in range(len(ans)):
    start = str(ans[i][0]/3600) + ':'
    val = ans[i][0]%3600
    start = start + str(val/60)+ ':'
    val = val%60
    start = start + str(val) 

    end = str(ans[i][1]/3600) + ':'
    val = ans[i][1]%3600
    end = end + str(val/60)+ ':'
    val = val%60
    end = end + str(val) 
    
    print(start,end)

#print(ans)
print(len(ans))
    