import os,re

path = "out/"

for (path, dirs, files) in os.walk(path):
	for file in files:
		if ".file" in file:
			logFid=open(file+".log.temp",'w')
			print file
			
			for line in open(path+file).readlines():
				line=line.lower()				
				try:
				  	#print line[line.index('=">')+3:].split('-')
				  	lst = line[line.index('=">')+3:].split('-')
				  	logFid.write("\n"+str(lst[0])+','+str(lst[1])+','+str(lst[2])+','+str(lst[5][:lst[5].index('</a>')])+',')
				except ValueError:
					length = len(line.split('>'))
					#print line.split('>')[length/2]
					logFid.write(line.split('>')[length/2]+',')
