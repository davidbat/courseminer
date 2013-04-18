import csv

# creates a hash of students id -> courses taken
# It finds only those students that are eligible to register
def create_student_hash(crn_hash, cid_hash, stud_hash):
	inv_cid_hash = {v:k for k, v in cid_hash.items()}
	lines = []
	with open("grad_info2.csv", 'rb') as csvfile:
		class_data = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in class_data:
			lines.append(row)
	
	stud_course = {}
	for each in lines:
		sem, crn, level, stud_id  = each
		if stud_id not in stud_hash: continue
		if crn_hash[sem].has_key(crn):
			if stud_course.has_key(stud_id):
				if crn_hash[sem][crn] != "UNWANTED":
					stud_course[stud_id].append(crn_hash[sem][crn])
			else:
				if crn_hash[sem][crn] != "UNWANTED":
					stud_course[stud_id] = [crn_hash[sem][crn]]

	spring_studs = map(lambda line:line.strip(), open('eligible_stud.txt').readlines())
	with open('stud_info.txt', 'w') as std:
		for studid in stud_course:
			if studid not in spring_studs:
				continue
			dupliates = filter(lambda x:stud_course[studid].count(x) > 1, stud_course[studid])
			if dupliates != []:
				print "Duplicate courses - ", " ".join(map(lambda item:inv_cid_hash[item], dupliates)), "taken by ", studid
			std.write(" ".join(map(lambda item:inv_cid_hash[item],stud_course[studid])) + "\n")
	return stud_course

# write the courses taken by previous students into courses.txt
def write_out(crn_hash, cid_hash, stud_hash):
	out = open("courses.txt", "w")
	stud_course = create_student_hash(crn_hash, cid_hash, stud_hash)
	for stud_id in stud_course:
		out.write(" ".join(stud_course[stud_id]) + "\n")
	out.close()

# The course enrollement data contains CRN's. We replace these with actual CID's.
def create_common_id(program = [ "MSCS Computer Science" ]):
	lines = []
	# Unwanted cids are courses like Coop, Disertation, Reading, Thesis.
	unwanted_cids = [ 	'CS1210', 'CS1501', 'CS1801', 'CS2501', 'CS2511', 'CS2801', 'CS2900', 'CS2901', 
						'CS4611', 'CS4991', 'CS4993', 'CS5011', 'CS5336', 'CS6949', 'CS7381', 'CS7990', 
						'CS7996', 'CS8674', 'CS8949', 'CS8982', 'CS8984', 'CS8986', 'CS9990', 'CS9996', 
						'IA5131', 'IA5151', 'IA5211', 'IA5978', 'IA5984', 'IA8982', 'CS6964',
						'BUSN1100','COOP3945','CS1210','CS1220','CS6949','CS6964','MATH3000','MATH4000' ]
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
			lines.append(row)
	sem_crn_hash={}
	cid_hash = {}
	new_id = 0
	for line_list in lines:
		sem = line_list[0]
		cid = line_list[8]
		crn = line_list[7]
		if sem_crn_hash.has_key(sem):
			if not sem_crn_hash[sem].has_key(crn):
				if cid in unwanted_cids:
					sem_crn_hash[sem][crn] = "UNWANTED"
				else:					
					if not cid_hash.has_key(cid):
						new_id += 1
						cid_hash[cid] = str(new_id)
					sem_crn_hash[sem][crn] = cid_hash[cid]
		else:
			if not cid_hash.has_key(cid):
				new_id += 1
				cid_hash[cid] = str(new_id)
			sem_crn_hash[sem] = { crn : cid_hash[cid] }
	for ids in cid_hash:
		fcid.write(cid_hash[ids] + " " + ids + "\n")
	write_out(sem_crn_hash, cid_hash, stud_hash)


if __name__ == "__main__":
	create_common_id()
