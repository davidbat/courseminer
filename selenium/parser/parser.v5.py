import os,re,sys

path = "../out/"

for (path, dirs, files) in os.walk(path):
        for file in files:
                if "Summer" not in file and ".file" in file:
                        logFid=open(file+".log",'w')
                        print file
                        crn=''
                        cid=''
			i=0
			flag = False
                        res=""
                        count=1
                        CapAct = ""                       
                        fileLines = open(path+file).readlines()
                        for line in open(path+file).readlines():
                                line=line.lower()
				if '=">' in line:
					temp = line[line.index('=">')+3:]																
					match = re.search('[0-9]{5} - [a-z]{4} [0-9]{4}', temp.split('(')[0])
                                        if match:
                                                crn=str(match.group(0).split("-")[0])
                                                cid=str(match.group(0).split("-")[1])
                                        lst = line[line.index('=">')+3:].split(' - ')
					credits = temp.split('credits')[1]
					#logFid.write(file.split(".file")[0]+','+'xyz,'+str(lst[0])+',0,'+credits[:credits.index('</a>')]+',')
                                        res=file.split(".file")[0].replace("_"," ")+','+'xyz,'+str(lst[0].replace(',','-'))+',0,'+credits[:credits.index('</a>')]+','        
					flag = True
                                elif '</span>' in line:
                                        #print file                
                                        #print line
                                        instr = line[line.index('</span>')+7:line.index('(<abbr')].split(" ")
        	                        #logFid.write(instr[0]+","+instr[len(instr)-2]+","+crn+","+cid.replace(' ','')+",")
                                        res+=instr[0]+","+instr[len(instr)-2]+","+crn+","+cid.replace(' ','')+","
					flag = False
				elif flag:
                                        #print "No instructor for " + cid + "," + crn
                                        #logFid.write("abc,def,"+crn+","+cid.replace(' ','')+",")
                                        res+="abc,def,"+crn+","+cid.replace(' ','')+","					
                                elif 'dddefault' in line:	
                                	temp = line.split('dddefault">')[1].split('</td')
                                        CapAct += temp[0] + ','
                                        if count % 4 == 0:
                                                logFid.write(res+CapAct+"\n")
                                                #print res
                                                CapAct=""
                                                count=0
                                        count+=1
                                        if i+1 <> len(fileLines) and '=">' in fileLines[i+1]:
                                        	#logFid.write('\n')
                                                #count=0
                                                res="" 
                                                #CapAct=""       
				i+=1
