import re 

def find_storyStart():
        datafile = open(r'../v.txt')
        f = open(r'../ss.txt','w')
        found = 0
        ignorecase = re.compile('Type=Story Start', re.IGNORECASE)
        for line in datafile:
            if ignorecase.search(line) : 
                found = found + 1
                time = str(3600*int(line[8:10])+60*int(line[10:12])+1*int(line[12:14]))+'-'+str(3600*int(line[27:29])+60*int(line[29:31])+int(line[31:33])-10)
                f.write(time+'\n')
                print(line)
                print(time)

               
        f.close()
        return found 


print(find_storyStart())
