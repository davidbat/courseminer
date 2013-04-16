#!/usr/bin/python
import sys
import csv
from constants import *

hm = {}
stud_hash = {}
program = [ "MSCS Computer Science" ]
if len(sys.argv) == 3:
		program = sys.argv[2:]

cur_sem = sys.argv[1]

# Return a list of previous semesters
def prev_sems(cur_sem):
	all_sems = ['Fall 2009', 'Spring 2010', 'Fall 2010', 'Spring 2011', 'Fall 2011', 'Spring 2012', 'Fall 2012', 'Spring 2013']
	cur_sem_indx = all_sems.index(cur_sem)
	return all_sems[:cur_sem_indx]


# This function will save the students in the current semester into stud_actual.txt
# It will also update the classes.out.csv with the students (UG/GR) that have taken 
# courses (for all semesters including the current semester.)
def calculate_students(cur_sem, lvl = 'GR', program=[ "MSCS Computer Science" ]):
	prior = {}
	avg_prior = {}

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
			slvl = enroll[2]
			if slvl != lvl:
				continue
			nid = enroll[3]
			if nid not in stud_hash:
				continue

			if sem not in hm:
				hm[sem] = {}
				hm[sem][crn] = {}
				hm[sem][crn][slvl] = 1
			else:
				if crn not in hm[sem]:
					hm[sem][crn] = {}
					hm[sem][crn][slvl] = 1
				else:
					if lvl in hm[sem][crn]:
						hm[sem][crn][slvl] += 1
					else:
						hm[sem][crn][slvl] = 1

	out_index = 10
	output = "classes.output.csv"
	out_fd = open(output, 'wb')
	output_actual = "stud_actual.txt"
	act_fd = open(output_actual, 'wb')
	total = {}
	actual_courses = {}
	#out = open(output, "w")
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
			if lvl == 'GR':
				val = grad
			else:
				val = undergrad
				#print val
			line.insert(out_index, str(val))
			#line.insert(out_index, str(grad))
			if sem not in total:
				total[sem] = 0.0

			total[sem] += val
			if sem not in prior:
				prior[sem] = { cid:val }
			elif cid not in prior[sem]:
	   			prior[sem][cid] = val
	   		else:
	   			prior[sem][cid] += val


	   		out.writerow(line)
			if sem == cur_sem and val != 0:
				if cid not in actual_courses:
					actual_courses[cid] = 0.0
				actual_courses[cid] += val

	for key, value in actual_courses.iteritems():
		act_fd.write(key + "\t" + str(value) + "\n")


	for sem in prev_sems(cur_sem) + [cur_sem]:
		# Ignore summer semesters
		if 'Summer' in sem:
			continue
		if sem == cur_sem:
			for cid in prior[sem]:
				if cid not in avg_prior:
					avg_prior[cid] = { 'val':0.0, 'cnt':1.0 }
			continue
		for cid in prior[sem]:
			if cid in avg_prior:
				avg_prior[cid]['val'] += prior[sem][cid] / total[sem]
				avg_prior[cid]['cnt'] += 1.0
			else:
				avg_prior[cid] = { 'val':prior[sem][cid] / total[sem] ,'cnt':1 }

	tot = 1.0
	smoother = tot / len(avg_prior) 
	for cid in avg_prior:
		avg_prior[cid] = (avg_prior[cid]['val'] + smoother) / (avg_prior[cid]['cnt'] + tot)

	act_fd.close()
	out_fd.close()
	return avg_prior

		
if __name__ == "__main__":
	calculate_students(cur_sem, program)