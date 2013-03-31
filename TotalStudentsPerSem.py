#!/usr/bin/python

hm = {}

for line in open('classes.temp.csv'):
	lst = line.split(',')
	# 9,10
	if hm.has_key(lst[0]):
		hm[lst[0]]+=int(lst[10])
	else:
		hm[lst[0]]=int(lst[10])

#fid=open('classes.output.csv','w')

for line in open('classes.temp.csv'):
	lst = line.split(',')[:-1]
	lst.insert(9,hm[lst[0]])
	string=''
	for l in lst:
		string+=str(l)+','	
	print string
	#fid.write(string)	
