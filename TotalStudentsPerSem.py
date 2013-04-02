#!/usr/bin/python
import sys
import csv
hm = {}

with open('CourseEnrollmentInfo.csv') as csvfile:
	enroll_data = csv.reader(csvfile, delimiter=',', quotechar='"')
	for enroll in enroll_data:
		sem = enroll[0]
		crn = enroll[1]
		lvl = enroll[2]
		if sem not in hm:
			hm[sem] = {}
			hm[sem][crn] = {}
			hm[sem][crn][lvl] = 1
		else:
			if crn not in hm[sem]:
				hm[sem][crn] = {}
				hm[sem][crn][lvl] = 1
			else:
				if lvl in hm[sem][crn]:
					hm[sem][crn][lvl] += 1
				else:
					hm[sem][crn][lvl] = 1
			

# max, grad, undergrad, actual
#fid=open('classes.output.csv','w')
out_index = 10
output = "classes.output.csv"
out_fd = open(output, 'wb')
output_actual = "stud_actual.txt"
act_fd = open(output_actual, 'wb')

#out = open(output, "w")
out = csv.writer(out_fd)
with open("classes.csv", 'rb') as csvfile:
	class_data = csv.reader(csvfile, delimiter=',', quotechar='"')
	for line in class_data:
		sem = line[0]
		crn = line[7]
		grad = 0
		undergrad = 0
		if crn in hm[sem]:
			if "Graduate" in hm[sem][crn]:
				grad = hm[sem][crn]['Graduate']
			if "Undergraduate" in hm[sem][crn]:
				undergrad = hm[sem][crn]['Undergraduate']
		line.insert(out_index, str(undergrad))
		line.insert(out_index, str(grad))
   		
   		out.writerow(line)
		if sem == sys.argv[1]:
            		act_fd.write(line[8] + "\t" + str(grad) + "\n")
			
		#csv.writer(file , delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
		#out.write(",".join(line) + "\n")
out_fd.close()
act_fd.close()
		
