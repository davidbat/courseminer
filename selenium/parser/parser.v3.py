import os,re,sys

path = "out/"

for (path, dirs, files) in os.walk(path):
	for file in files:
		if "Fall_2009.file" in file:
			logFid=open(file+".log",'w')
			print file
			count = 0
			flag = False
			for line in open(path+file).readlines():
				line=line.lower()
				try:
				  print line[line.index('=">')+3:].split('-')
				  lst = line[line.index('=">')+3:].split('-')
				  if count < 7:
					count = 0	
				  logFid.write("\n"+str(lst[0])+','+str(lst[1])+','+str(lst[2])+','+str(lst[5][:lst[5].index('</a>')].split(" ")[-1])+',')
				  count = 0
				  print count				
				except ValueError:
					if count < 6 and not flag:		 
                                        	length = len(line.split('>'))
                                        	print line.split('>')[length/2]
                                        	logFid.write(line.split('>')[length/2]+',')
	                                        count+=1
						#print count
				  	else:
						try:
                		                  print line[line.index('=">')+3:].split('-')
                                                  print "split happened here2"

		                                  lst = line[line.index('=">')+3:].split('-')
                               		          logFid.write("\n"+str(lst[0])+','+str(lst[1])+','+str(lst[2])+','+str(lst[5][:lst[5].index('</a>')].split(" ")[-1])+',')
						  count=1
						except ValueError:
						  #print "count is"
						  #print count
						  if count < 10:
							flag = True
						        length = len(line.split('>'))
                                                	print line.split('>')[length/2]
                                                	logFid.write(line.split('>')[length/2]+',')
                                                	count+=1
						  else: 
							flag=False	
						        count = 0
	                                          	try:
						    #print "flag is "
						    #print flag
 	                                                   lst = line[line.index('=">')+3:].split('-')
						  	except ValueError:
		        				  print "Some error in parsed data..."
							  print line
							  sys.exit(2)
				
	
