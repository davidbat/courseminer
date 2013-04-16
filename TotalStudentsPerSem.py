#!/usr/bin/python
import sys
import csv

# This function will save the students in the current semester into stud_actual.txt
# It will also update the classes.out.csv with the students (UG/GR) that have taken 
# courses (for all semesters including the current semester.)
def calculate_students(cur_sem, level = 'GR', program = [ "MSCS Computer Science" ]):
	hm = {}
	stud_hash = {}
	with open('Student_Information.csv') as studfile:
		for line in studfile.readlines():
			stud = line.strip().split(",")
			if stud[1] in program: 
				stud_hash[stud[5]] = stud[1]


	with open('CourseEnrollmentInfo.csv') as csvfile:
		enroll_data = csv.reader(csvfile, delimiter=',', quotechar='"')
		for enroll in enroll_data:
			sem = enroll[0]
			crn = enroll[1]
			lvl = enroll[2]
			nid = enroll[3]
			if nid not in stud_hash:
				continue

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
				

	out_index = 10
	output = "classes.output.csv"
	out_fd = open(output, 'wb')
	output_actual = "stud_actual.txt"
	act_fd = open(output_actual, 'wb')
	actual_courses = {}
	out = csv.writer(out_fd)
	with open("classes.csv", 'rb') as csvfile:
		class_data = csv.reader(csvfile, delimiter=',', quotechar='"')
		for line in class_data:
			sem = line[0]
			crn = line[7]
			cid = line[8]
			grad = 0
			undergrad = 0
			if sem in hm and crn in hm[sem]:
				if "GR" in hm[sem][crn]:
					grad = hm[sem][crn]['GR']
				if "UG" in hm[sem][crn]:
					undergrad = hm[sem][crn]['UG']
			if level == 'UG':
				val = undergrad
			else:
				val = grad
				
	   		line.insert(out_index, str(val))
	   		out.writerow(line)
			if sem == cur_sem and val != 0:
				if cid not in actual_courses:
					actual_courses[cid] = 0.0
				actual_courses[cid] += val
				
	for key, value in actual_courses.iteritems():
		act_fd.write(key + "\t" + str(value) + "\n")
	out_fd.close()
	act_fd.close()
		
if __name__ == "__main__":
	sem = sys.argv[1]
	level = sys.argv[2]
	calculate_students(sem, level)