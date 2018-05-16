#this file is especially for testing various logics and then selecting the best one

f = file('ans.txt')
mus = []
count = 0
for line in f :
    temp =  line.split('-')
    if int(temp[1])-int(temp[0]) < 16:
        mus.append([int(temp[0]), int(temp[1])])
        count = count + 1
f.close()
f = open('ans1.txt','w')
f.write(mus)
f.close
