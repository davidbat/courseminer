import csv


def create_common_id(program):
	unwanted_cids = ['CS6949', 'CS6964', 'CS5011']
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


def prev_sems(cur_sem):
	all_sems = ['Fall 2009', 'Spring 2010', 'Fall 2010', 'Spring 2011', 'Fall 2011', 'Spring 2012', 'Fall 2012', 'Spring 2013']
	cur_sem_indx = all_sems.index(cur_sem)
	return all_sems[:cur_sem_indx]

def students_in_program(program, cur_sem):
	student_sem_list = {}
	previous_sem = prev_sems(cur_sem)
	for stud in ReadFile('Student_Information.csv'):
		if stud[1] in program and stud[0] in previous_sem \
			and stud[4] == "Eligible to Register":
			if stud[0] in student_sem_list:
				student_sem_list[stud[0]].append(stud[-1])
			else:
				student_sem_list[stud[0]] = [ stud[-1] ]
	#print stud_hash
	return student_sem_list

def ReadFile(fn, delim = ","):
	features = []
	for line in open(fn).readlines():
		features.append(map(lambda i: i, line.strip().split(delim)))
	return features

def read_grad_info(program, cur_sem, lvl):	
	crn_hash = create_common_id(program)
	
	grad_hash = {}
	for line in ReadFile("CourseEnrollmentInfo.csv"):
		sem = line[0]
		sid = line[-1]
		slvl = line[2]

		if line[1] not in crn_hash[sem].keys():
			#print sorted(crn_hash[sem].keys())
			print "Could not find CRN for - ", line[1], sem
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

def stud_sem_wise_course_map(program, cur_sem, lvl):
	student_hash = {}
	student_sem_list = students_in_program(program, cur_sem)
	grad_hash = read_grad_info(program, cur_sem, lvl)
	for sem in prev_sems(cur_sem):
		for stud_id in student_sem_list[sem]:
			if stud_id in student_hash:
				for sems in sorted(student_hash[stud_id].keys()):
					if student_hash[stud_id][sems] == []:
						# print stud_id, sem, sems
						# We assume that if stud_id is not in the grad_hash for 
						# that sem then the student is Eligible to register but has
						# taken only a Coop (or one of the unwanted) courses
						if stud_id in grad_hash[sem]:
							student_hash[stud_id][sems] = grad_hash[sem][stud_id]
						break
			else:
				student_hash[stud_id] = { 'sem1':[], 'sem2':[], 'sem3':[], 'sem4':[] }
				if stud_id in grad_hash[sem]:
					student_hash[stud_id]['sem1'] = grad_hash[sem][stud_id]

	print student_hash

if __name__ == "__main__":
	dunno([ 'MSCS Computer Science' ], "Spring 2013", "Graduate")


