import os,re,sys

path = "../out/"

for (path, dirs, files) in os.walk(path):
	for file in files:
		if "Fall_2009.file" in file:
			logFid=open(file+".log",'w')
			count = 0
			print file
			crn=''
			cid=''
			for line in open(path+file).readlines():
				line=line.lower()				
				try:
					#print line
				  	lst = line[line.index('attr=">')+7:].split('-')
					#logFid.write("\n"+str(lst[0])+','+str(lst[1])+','+str(lst[2])+','+str(lst[5][:lst[5].index('</a>')])+',')
					logFid.write("\n"+file.split(".file")[0]+','+'xyz,'+str(lst[0])+',0,'+str(lst[5][:lst[5].index('</a>')]).split(" ")[2]+',')
					crn=str(lst[1])
					cid=str(lst[2])	
				except ValueError:
					try:
						instr = line[line.index('</span>')+7:line.index('(<abbr')]
                                                logFid.write(instr.replace(" ",",")+crn+","+cid.replace(' ','')+",")	
					except ValueError:
						if count < 4:
							#print  str(count) +"-"+ line
							length = len(line.split('>'))
							temp = line.split('>')[length/2]
							logFid.write(temp[:-4]+',')
							count+=1
							continue					
						try:
							lst = line[line.index('attr=">')+7:].split('-')
							count=0
						except ValueError:
							try:
								line.index('dddefault')
							except ValueError:
								sys.exit(2)	
							count=0	
						
										

