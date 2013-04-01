import os,re,sys,glob

path = "../out/"

def lrStrip(mystr):
	return mystr.lstrip().rstrip()

for my_random in [1]:
	for file in ["Fall_2009.file", "Fall_2010.file", "Fall_2011.file", "Fall_2012.file", "Spring_2010.file", "Spring_2011.file", "Spring_2012.file", "Spring_2013.file"]:
		print file
		if "Summer" not in file:
			logFid=open(file+".out",'w')
			print file
			itr=0	
			crn=''
			cid=''
			i=0
			flag = False
			res=""
			count=1
			CapAct = ""                       
			fileLines = open(path+file).readlines()

			while itr < len(fileLines):
				#print fileLines[itr]
				line=fileLines[itr]
				if '=">' in line:
					match = re.search('=">.+</a>',line)
					temp = match.group(0)            
					match = re.search('[0-9]{5} - [a-zA-Z]{0,4} [0-9]{0,4}', temp)
					credits = lrStrip(temp.split('Credits')[1].split('</a>')[0])
					crn=lrStrip(match.group(0).split("-")[0])
					courseName = lrStrip(lrStrip(temp.split(crn)[0][3:])[:-1]).replace(",","|")    
					cid=lrStrip(match.group(0).split("-")[1])
					res=file.split(".file")[0].replace("_"," ")+','+'xyz,'+courseName+',0,'+credits+','
					flag = True
					itr += 1
				elif '</span>' in line:
					instr = line[line.index('</span>')+7:line.index('(<abbr')].split(" ")
					res+=instr[0]+","+instr[len(instr)-2]+","+crn+","+cid.replace(' ','')+","
					flag = False
					itr += 1
				elif flag:
					res+="abc,def,"+crn+","+cid.replace(' ','')+","	
					flag = False
				elif 'dddefault' in line:
					CapAct = []
					while 'dddefault' in line and itr < len(fileLines)  :
				
						temp = line.split('dddefault">')[1].split('</td')
						#print temp
						CapAct.append(temp[0])
						itr+=1
						if itr < len(fileLines) :
							line = fileLines[itr]

					#print "CapAct:"
					
					if len(CapAct) % 4 == 0:
					#	print CapAct
						for i in range(len(CapAct) / 4):
							#outline = res+",".join(CapAct[i*4:i*4+2])+",\n"
							logFid.write(res+",".join(CapAct[i*4:i*4+2])+",\n")
					else:
					#	print CapAct
					 	print res																														
				
