import csv
def create_student_hash(crn_hash):
	lines = []
	with open("grad_info.csv", 'rb') as csvfile:
		class_data = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in class_data:
			#print row
			lines.append(row)
	
	stud_course = {}
	for each in lines:
		#print each
		sem, crn, level, stud_id  = each

		#print sem, crn, level, stud_id, crn_hash[sem][crn]
		if crn_hash[sem].has_key(crn):
			if stud_course.has_key(stud_id):
				stud_course[stud_id].append(crn_hash[sem][crn])
			else:
				stud_course[stud_id] = [crn_hash[sem][crn]]
		else:
			print "CRN - ", crn, " is not present in the list of CRNS-CIDS"
	return stud_course

#print sem_stud_course
def write_out(crn_hash):
	out = open("courses.txt", "w")
	stud_course = create_student_hash(crn_hash)
	for stud_id in stud_course:
		out.write(" ".join(stud_course[stud_id]) + "\n")
	out.close()


def create_common_id():
	lines = []
	fcid = open("CID_hash.txt", "w")
	with open("classes.csv", 'rb') as csvfile:
		class_data = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in class_data:
			#print row
			lines.append(row)
	#out = open("common_crn_file.txt","w")
	sem_crn_hash={}
	cid_hash = {}
	new_id = 0
	#print lines
	for line_list in lines:
		#line_list = line.split(",")
		#acad,course,title,min_cred,max_cred,f_name,l_name,crn,cid,max_cap,act_cap,meet_time
		sem = line_list[0]
		cid = line_list[8]
		crn = line_list[7]
		#print cid, crn
		if sem_crn_hash.has_key(sem):
			if sem_crn_hash[sem].has_key(crn):
				print "CRN ", crn, " has multiple courses in semsester - ", sem, ". Course ids are - ", cid, sem_crn_hash[sem][crn] 
			else:
				if not cid_hash.has_key(cid):
					new_id += 1
					cid_hash[cid] = str(new_id)
				sem_crn_hash[sem][crn] = cid_hash[cid]
				
			#crn_hash[crn].append(crn)	
		else:
			if not cid_hash.has_key(cid):
				new_id += 1
				cid_hash[cid] = str(new_id)
			sem_crn_hash[sem] = { crn : cid_hash[cid] }
	#print sem_crn_hash
	for ids in cid_hash:
		fcid.write(cid_hash[ids] + " " + ids + "\n")
	write_out(sem_crn_hash)

create_common_id()
