import os,re

path = "out/"


for (path, dirs, files) in os.walk(path):
	for file in files:
		if "Summer_2_2012.file" in file:
			logFid=open(file+".log",'w')
			count = 0 
			print file
			
			for line in open(path+file).readlines():
				line=line.lower()				
				try:	
					print line[line.index('=">')+3:].split('-')
					logFid.write("\n"+str(line[line.index('=">')+3:].split('-'))+',')
				except ValueError:
					length = len(line.split('>'))
					print line.split('>')[length/2]
					logFid.write(line.split('>')[length/2]+',')

