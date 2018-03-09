def find_commercials():
        datafile = file('subtitles.txt3')
        f = open('commercials_secs.txt','w')
        found = 0
        for line in datafile:
            if 'SEG_00|Type=Commercial' in line: 
                found = found + 1
                start = (int(line[8:10])*3600)+int(line[10:12])*60+int(line[12:14])
                end = (int(line[27:29])*3600)+int(line[29:31])*60+int(line[31:33])
                print(start, end)
                line = str(start)+'-'+str(end)
                f.write(line+'\n')
                print(line)
               
        f.close()
        return found 


print find_commercials()