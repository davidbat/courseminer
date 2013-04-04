#!/usr/bin/python

fid = open('dump','w')

for line in open(classes.csv):
	line = line.split(",")
	for i in range(len(line)):
		if i == 0:
			if line[i] == "Fall 2009":
				fid.write("1,0,0,0,0,0,0,0,")
			if line[i] == "Spring 2010":
				fid.write("0,1,0,0,0,0,0,0,")
			if line[i] == "Fall 2010":
				fid.write("0,0,1,0,0,0,0,0,")
			if line[i] == "Spring 2011":
				fid.write("0,0,0,1,0,0,0,0,")
			if line[i] == "Fall 2011":
				fid.write("0,0,0,0,1,0,0,0,")				
			if line[i] == "Spring 2012":
				fid.write("0,0,0,0,0,1,0,0,")
			if line[i] == "Fall 2012":
				fid.write("0,0,0,0,0,0,1,0,")
			if line[i] == "Spring 2013":
				fid.write("0,0,0,0,0,0,0,1,")

		if i == 1:
			if line[i] == "Bouve College of Hlth Sciences"


		
		