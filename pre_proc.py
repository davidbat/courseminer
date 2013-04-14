import csv

def create_student_hash(crn_hash, cid_hash, stud_hash):
	inv_cid_hash = {v:k for k, v in cid_hash.items()}
	lines = []
	with open("grad_info2.csv", 'rb') as csvfile:
		class_data = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in class_data:
			#print row
			lines.append(row)
	
	stud_course = {}
	for each in lines:
		#print each
		sem, crn, level, stud_id  = each
		if stud_id not in stud_hash: continue
		#print sem, crn, level, stud_id, crn_hash[sem][crn]
		if crn_hash[sem].has_key(crn):
			if stud_course.has_key(stud_id):
				if crn_hash[sem][crn] != "UNWANTED":
					stud_course[stud_id].append(crn_hash[sem][crn])
			else:
				if crn_hash[sem][crn] != "UNWANTED":
					stud_course[stud_id] = [crn_hash[sem][crn]]
		#else:
		#	print "CRN - ", crn, " is not present in the list of CRNS-CIDS"

	spring_studs = map(lambda line:line.strip(), open('eligible_stud.txt').readlines())
	#print spring_studs
	with open('stud_info.txt', 'w') as std:
		for studid in stud_course:
			#print studid
			if studid not in spring_studs:
				continue
			dupliates = filter(lambda x:stud_course[studid].count(x) > 1, stud_course[studid])
			if dupliates != []:
				print "Duplicate courses - ", " ".join(map(lambda item:inv_cid_hash[item], dupliates)), "taken by ", studid
			std.write(" ".join(map(lambda item:inv_cid_hash[item],stud_course[studid])) + "\n")
	return stud_course

#print sem_stud_course
def write_out(crn_hash, cid_hash, stud_hash):
	out = open("courses.txt", "w")
	stud_course = create_student_hash(crn_hash, cid_hash, stud_hash)
	for stud_id in stud_course:
		out.write(" ".join(stud_course[stud_id]) + "\n")
	out.close()


def create_common_id(program = [ "MSCS Computer Science" ]):
	lines = []
	unwanted_cids = ['CS6949', 'CS6964', 'CS5011', 'BUSN1100','COOP3945',
			'CS1210','CS1220','CS6949','CS6964','MATH3000','MATH4000' ]
	fcid = open("CID_hash.txt", "w")

	stud_hash = {}
	with open('Student_Information.csv') as studfile:
		for line in studfile.readlines():
			stud = line.strip().split(",")
			if stud[1] in program: 
				stud_hash[stud[5]] = stud[1]

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
			if not sem_crn_hash[sem].has_key(crn):
			#	print "CRN ", crn, " has multiple courses in semsester - ", sem, ". Course ids are - ", cid, sem_crn_hash[sem][crn] 
			#else:
				if cid in unwanted_cids:
					sem_crn_hash[sem][crn] = "UNWANTED"
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
	write_out(sem_crn_hash, cid_hash, stud_hash)


if __name__ == "__main__":
	create_common_id()
