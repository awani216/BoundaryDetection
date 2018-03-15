import numpy as np

commercial = file('ans1.txt')
music =  file('story_start.txt')
com = []
mus = [] 
for line in commercial:
    temp =  line.split('-')
    com.append([int(temp[0]), int(temp[1])])

for line in music:
    temp =  line.split('-')
    mus.append([int(temp[0]), int(temp[1])])
res = []

for i in range(len(mus)):
    for j in range(len(com)):
        if (mus[i][0]>=com[j][0]) and (mus[i][1]<=com[j][1]):
            res.append(i)

ans = np.delete(mus, res, 0)
count = 0
fres = open('ans.txt','w') 
for i in range(len(ans)):
    line = str(ans[i][0]) + '-' + str(ans[i][1])
    fres.write(line +  '\n')
    count = count + 1
fres.close()


print(len(com))
print(len(mus))
print(ans)
print(count)

 