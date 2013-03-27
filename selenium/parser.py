import os,re

path = "out/"

for (path, dirs, files) in os.walk(path):
	for file in files:
		if "Fall_2009.file" in file:
			count = 0 
			print file
			extraCourses = False			
			
			for line in open(path+file).readlines():
				line=line.lower()
				#print "last"+line
                                if count%6 == 0 and '<td ' in line and 'colgroup' not in line:
					print line
					print 'entered1'
					extraCourses = True
				else:
					count+=2
					extraCourses = False
				
                                if count%6 == 0 and extraCourses == False:
					print 'entered2'
					print line[line.index('=">')+3:].split('-')
					count+=1

                                elif count%6 == 1 and extraCourses == False:
					print line
                                        count+=1

                                elif count%6 == 2 and extraCourses == False:
					print line
	                                count+=1

                                elif count%6 == 3 and extraCourses == False:
					print line
	                                count+=1

                                elif count%6 == 4 and extraCourses == False:
					print line
	                                count+=1

                                elif count%6 == 5 and extraCourses == False:
					print line
					count+=1
							

