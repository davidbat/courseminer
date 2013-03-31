#!/usr/bin/python

import os

path = "/home/rushabh/courseminer/courseminer/selenium/parser/"

for (path, dirs, files) in os.walk(path):
        for file in files:
		if ".log" in file:
			hm = {}
			print file
			
			for line in open(path+file):
				lst = line.split(',')
				# 9,10
				if hm.has_key(lst[0]):
        	                        if "n/a" not in lst[10]:
						hm[lst[0]]+=int(lst[10])
                                        else:	
						hm[lst[0]]+=0		
				else:
                                        if "n/a" not in lst[10]:
                                                hm[lst[0]]=int(lst[10])
                                        else:   
                                                hm[lst[0]]=0

				
				fid=open(path+file+'.total','w')
					
			for line in open(path+file):
				lst = line.split(',')[:-1]
				
				lst.insert(9,hm[lst[0]])
				string=''
				for l in lst:
					string+=str(l)+','	
				#print string
				fid.write(string+'\n')	
