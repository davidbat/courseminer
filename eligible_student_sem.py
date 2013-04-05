import sys


#program = ['MS Health Informatics']

def ReadFile(fn, delim = ","):
	features = []
	for line in open(fn).readlines():
		features.append(map(lambda i: i, line.strip().split(delim)))
	return features

def eligible_students(program, sem, lvl):
	registration = "Eligible to Register"
	es = open("eligible_stud.txt", "w")

	# No extra commas in file so don't need CSV reader
	all_students = "Student_Information.csv"
	#print ReadFile(all_students)
	sem_stud_dump = filter(lambda row: sem in row[0] and row[1] in program and row[3] == lvl and row[4] == registration, ReadFile(all_students))
	#sem_stud_dump = filter(lambda row: sem in row[0] and row[3] == lvl and row[4] == registration, ReadFile(all_students))
	new_student = 0

	for stud in sem_stud_dump:
		if sem in stud[2]:
			new_student += 1
		else:
			es.write(stud[5] + "\n")

	es.close()
	return new_student


if __name__ == "__main__":
	sem = sys.argv[1] 
	lvl = sys.argv[2]
	program = sys.argv[3:]
	new_student = eligible_students(program, sem, lvl)
	print "new_student=",new_student