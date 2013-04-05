import sys
import csv

def cur_students_in_program(program, cur_sem):
	stud_hash = {}
	with open('Student_Information.csv') as studfile:
		for line in studfile.readlines():
			stud = line.strip().split(",")
			if cur_sem in stud[0] and stud[1] in program: 
				stud_hash[stud[5]] = stud[1]
	return stud_hash

def create_student_hash(program, cur_sem):
	stud_hash = cur_students_in_program(program, cur_sem)
	crn_hash = create_common_id(program, cur_sem)
	lines = []
	with open("grad_info.csv", 'rb') as csvfile:
		class_data = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in class_data:
			if row[0] == cur_sem:
				lines.append(row)
	
	stud_course = {}
	for each in lines:
		#print each
		sem, crn, level, stud_id  = each
		if stud_id not in stud_hash: 
			#print "This should not have happened, with studid -", stud_id
			continue
		#print sem, crn, level, stud_id, crn_hash[sem][crn]
		if crn_hash.has_key(crn):
			if stud_id not in stud_course:
				stud_course[stud_id] = [crn_hash[crn]]
			else:
				stud_course[stud_id].append(crn_hash[crn])
		else:
			print "CRN - ", crn, "for ", sem, " is not present in the list of CRNS-CIDS"

	return stud_course




def create_common_id(program, cur_sem):
	unwanted_cids = ['CS6949', 'CS6964', 'CS5011']
	lines = []
	crn_hash = {}
	with open("classes.csv", 'rb') as csvfile:
		class_data = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in class_data:
			sem = row[0]
			cid = row[8]
			crn = row[7]

			if sem == cur_sem and cid not in unwanted_cids:
				crn_hash[crn] = cid 
	return crn_hash


if __name__ == "__main__":
	program = [ 'MSCS Computer Science' ]
	if len(sys.argv) >= 3:
		program = sys.argv[2:]
	print create_student_hash(program, sys.argv[1])