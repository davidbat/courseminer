import os,re

path = "../out/"

for (path, dirs, files) in os.walk(path):
        for file in files:
                if "Fall_2009.file" in file:
                        logFid=open(file+".log",'w')
			print file
			lines = open(path+file).read().split('\n')
			for line in lines:
				line=line.lower()				
				try:
					if '13363' in line:
						print line[line.index('=">')+3:].split('-')
						print "res0"
						print lst[0]

                                                print "res1"
						print lst[1]

                                                print "res2"
						print lst[2]

                                                print "res3"
						print lst[5][:lst[5].index('</a>')]				
	
					lst = line[line.index('=">')+3:].split('-')
				  	logFid.write("\n\n"+str(lst[0])+','+str(lst[1])+','+str(lst[2])+','+str(lst[5][:lst[5].index('</a>')])+',')
				except ValueError:
					length = len(line.split('>'))
					logFid.write(line.split('>')[length/2]+',')
