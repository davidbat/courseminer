import csv
from constants import *

def create_common_id(program):
	# all the coops
	
	lines = []
	crn_hash = {}
	with open("classes.csv", 'rb') as csvfile:
		class_data = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in class_data:
			sem = row[0]
			cid = row[8]
			crn = row[7]

			if cid not in unwanted_cids:
				if sem in crn_hash:
					crn_hash[sem][crn] = cid
				else:
					crn_hash[sem] = { crn:cid }
	return crn_hash

# Return a list of previous semesters
def prev_sems(cur_sem):
	all_sems = ['Fall 2009', 'Spring 2010', 'Fall 2010', 'Spring 2011', 'Fall 2011', 'Spring 2012', 'Fall 2012', 'Spring 2013']
	cur_sem_indx = all_sems.index(cur_sem)
	return all_sems[:cur_sem_indx]

# Find the studnets who are eligible to register for the previous semester and program
# if current_flag = True, then we return only those students whi are eligible to register
# for the current semester
def students_in_program(program, cur_sem, current_flag=False):
	student_sem_list = {}
	previous_sem = prev_sems(cur_sem)
	if current_flag:
		previous_sem = [cur_sem]
	for stud in ReadFile('Student_Information.csv'):
		if stud[1] in program and stud[0] in previous_sem \
			and stud[4] == "Eligible to Register":
			if stud[0] in student_sem_list:
				student_sem_list[stud[0]].append(stud[-1])
			else:
				student_sem_list[stud[0]] = [ stud[-1] ]
	return student_sem_list

# read a file into a list
def ReadFile(fn, delim = ","):
	features = []
	for line in open(fn).readlines():
		features.append(map(lambda i: i, line.strip().split(delim)))
	return features

# Read the enrollment info and save it as a hash.
# sem -> stud_id -> [crns of courses taken]
def read_grad_info(program, cur_sem, lvl):
	crn_hash = create_common_id(program)
	
	grad_hash = {}
	for line in ReadFile("CourseEnrollmentInfo.csv"):
		sem = line[0]
		sid = line[-1]
		slvl = line[2]

		if line[1] not in crn_hash[sem].keys():
			continue
		crn = crn_hash[sem][line[1]]
		if slvl == lvl:
			if sem in grad_hash:
				if sid in grad_hash[sem]:
					grad_hash[sem][sid].append(crn)
				else:
					grad_hash[sem][sid] = [crn]
			else:
				grad_hash[sem] = { sid:[crn] }
	return grad_hash

# Create a hash of stud_id -> stud_sem -> [courses taken]
# here stud_sem if sem1..sem4 for GR and sem1..sem7 for UG
def stud_sem_wise_course_map(program, cur_sem, lvl, current_flag=False):
	SEMS_TO_TAKE = [ 'sem1', 'sem2', 'sem3', 'sem4' ]
	if lvl == "UG":
		SEMS_TO_TAKE += [ 'sem5', 'sem6', 'sem7']
	student_hash = {}
	uniq_courses = []
	prev_sems_stud_sem_list = students_in_program(program, cur_sem, False)
	student_sem_list = students_in_program(program, cur_sem, current_flag)
	grad_hash = read_grad_info(program, cur_sem, lvl)
	previous_sem = prev_sems(cur_sem)
	if current_flag:
		previous_sem += [cur_sem]
	for sem in previous_sem:		
		if current_flag:
			stud_list = student_sem_list[cur_sem]
		else:
			stud_list = student_sem_list[sem]
		for stud_id in stud_list:
			if stud_id in student_hash:
				for sems in sorted(student_hash[stud_id].keys()):
					if student_hash[stud_id][sems] == []:
						# We assume that if stud_id is not in the grad_hash for 
						# that sem then the student is Eligible to register but has
						# taken only a Coop (or one of the unwanted) courses
						if stud_id in grad_hash[sem] and (sem == cur_sem or stud_id in prev_sems_stud_sem_list[sem]):
							student_hash[stud_id][sems] = grad_hash[sem][stud_id]
							uniq_courses += student_hash[stud_id][sems] 
						break
			else:
				student_hash[stud_id] = {}
				for stud_sem in SEMS_TO_TAKE:
					student_hash[stud_id][stud_sem] = []
				if stud_id in grad_hash[sem]:
					student_hash[stud_id]['sem1'] = grad_hash[sem][stud_id]
	return list(set(uniq_courses)), student_hash

if __name__ == "__main__":
	(a,b) = stud_sem_wise_course_map([ 'MSCS Computer Science' ], "Spring 2013", "Graduate",True)
	print a, b

