def find_commercials():
        datafile = file('subtitles.txt3')
        f = open('commercials.txt','w')
        found = 0
        for line in datafile:
            if 'Type=Commercial' in line: 
                found = found + 1
                line = str(3600*int(line[8:10])+60*int(line[10:12])+1*int(line[12:14])+10)+'-'+str(3600*int(line[27:29])+60*int(line[29:31])+int(line[31:33])-10)
                f.write(line+'\n')
                print(line)
               
        f.close()
        return found 


print find_commercials()
