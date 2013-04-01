import sys

def ReadFile(fn):
	features = []
	for line in open(fn).readlines():
		features.append(map(lambda i: i, line.split(",")))
	return features

sem = sys.argv[1] 
lvl = sys.argv[2]
registration = "Eligible to Register"
program = "Computer Science"

es = open("eligible_stud.txt", "w")

# No extra commas in file so don't need CSV reader
all_students = "Student_Information.csv"
#print ReadFile(all_students)
sem_stud_dump = filter(lambda row: sem in row[0] and program in row[1] and row[3] == lvl and row[4] == registration, ReadFile(all_students))
new_student = 0

for stud in sem_stud_dump:
	if sem in stud[2]:
		new_student += 1
	else:
		es.write(stud[5])

es.close()

print "new_student=",new_student