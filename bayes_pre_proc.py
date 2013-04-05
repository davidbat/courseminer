import sys
import TotalStudentsPerSem as TSP
import pre_proc as PP
import csv
import eligible_student_sem as ES
import actual_labels as AL
import math

DUMMY = 999
cur_sem = sys.argv[1]
program = [ 'MSCS Computer Science' ]
all_sems = ['Fall 2009', 'Spring 2010', 'Fall 2010', 'Spring 2011', 'Fall 2011', 'Spring 2012', 'Fall 2012', 'Spring 2013']

#Exits with a ValueError exceptions when the sem is not found.
cur_sem_indx = all_sems.index(cur_sem)


TSP.calculate_students(cur_sem, program)


def find_unique(lst):
	all_items = []
	for line in lst:
		all_items += line
	return list(set(all_items))

def write_out_grad_info2():
	lines = []
	
	with open("grad_info.csv", 'rb') as csvfile:
			class_data = csv.reader(csvfile, delimiter=',', quotechar='"')
			for row in class_data:
				if row[0] in all_sems[:cur_sem_indx]:
					lines.append(row)
	fd = open("grad_info2.csv", 'w')
	for line in lines:
		fd.write(",".join(line) + "\n")
	fd.close()


def get_frequent_pairs():
	return map(lambda row:row[:-1] ,ES.ReadFile("frequent_pairs.txt", " "))

# Need to create grad_info2.csv before calling pre_proc.py
write_out_grad_info2()
# Need elgiible studnets for pre_proc
new_students = ES.eligible_students(program, cur_sem, "GR")
PP.create_common_id(program)

student_course_map = ES.ReadFile("courses.txt", " ")
uniq_courses = find_unique(map(lambda row:row[1:], student_course_map))
#print uniq_courses
frequent_pairs = get_frequent_pairs()

'''
if cur_sem_indx == -1:
	print "Semester -", cur_sem, "not found."
	exit()
	'''

def course_label(uniq_courses, label_course, student_course_map):
	base_indx = len(uniq_courses)
	#print label_course
	dummmy_indices = [ uniq_courses.index(label_course) ]
	lines = []
	#for fp in filter(lambda courses:courses if label_course in courses, frequent_pairs):
	#	dummmy_indices += [ frequent_pairs.index(fp) ]
	#>>> filter(lambda (index, courses): label_course in courses, enumerate(frequent_pairs))
	#	 [(0, [1, 2]), (1, [1, 3]), (2, [1, 4])]

	dummmy_indices += map(lambda r:r[0] + base_indx,filter(lambda (index, courses): label_course in courses, enumerate(frequent_pairs)))
	#print dummmy_indices
	for student_row in student_course_map:
		stud_id = student_row[0]
		courses_taken = student_row[1:]
		line = map(lambda course:1 if course in courses_taken else 0,uniq_courses) + \
				map(lambda courses:1 if courses[0] in courses_taken and courses[1] in courses_taken else 0, frequent_pairs) + \
				[ 1 if label_course in  courses_taken else 0 ]
		for index in dummmy_indices:
			line[index] = DUMMY
		lines.append(line)

	return lines

#	for sem in all_sems[:cur_sem_indx]

def bayes(db, means, test, prior_spam):
  bern_db = []
  #for each in db:
  # bern_db.append(map(lambda val, mean:int(val > mean) , each, attributes))
  # for every feature
  num_features = len(db[0]) - 1
  num_spam = sum(map(lambda val:val[-1], db))
  num_nspam = len(db) - num_spam
  alph = 1.0 / num_features
  d = num_features
  # for every feature
  for i in range(len(db[0]) - 1):
    inner = []
    p_less_spam = (map(lambda val:int((val[i] <= means[i]) & (val[-1] == 1)), db).count(1) + alph) / (num_spam + alph * d)
    p_more_spam = 1 - p_less_spam
    #p_more_spam = float(map(lambda val:int((val[i] > means[i]) & (val[-1] == 1)), db).count(1) + alph) / (num_spam + alph * d)
    p_less_nspm = (map(lambda val:int((val[i] <= means[i]) & (val[-1] == 0)), db).count(1) + alph) / (num_nspam + alph * d)
    p_more_nspm = 1 - p_less_nspm
    #p_more_nspm = (map(lambda val:int((val[i] > means[i]) & (val[-1] == 0)), db).count(1) + alph) / (num_nspam + alph * d)
    inner = [p_less_spam, p_more_spam, p_less_nspm, p_more_nspm]
    #if p_less_spam ==0 or p_more_spam ==0 or p_less_nspm == 0 or p_more_nspm == 0 or p_less_spam+p_more_spam <= .99 or p_less_spam+p_more_spam >= 1.01:
    #  print inner
    #print inner
    bern_db.append(inner)
  #print bern_db

  FP = 0
  FN = 0
  P = float(map(lambda row:row[-1], test).count(1))
  N = len(test) - P
  TP = 0
  TN = 0
  tau = []
  for row in test:
    spam = math.log(prior_spam, 2)
    nspam = math.log((1 - prior_spam), 2)
    for i in range(len(test[0]) - 1):
      #if bern_db[i][0] * bern_db[i][1] * bern_db[i][2] * bern_db[i][3] == 0:
      # print bern_db[i]
      if row[i] <= means[i]:
        spam += math.log(bern_db[i][0], 2)
        nspam += math.log(bern_db[i][2], 2)
      else:
        spam += math.log(bern_db[i][1], 2)
        nspam += math.log(bern_db[i][3], 2)
    tau.append([spam - nspam, row[-1]])
    if spam > nspam:
      # prediction is spam but it actually isn't then FP
      if row[-1] != 1:
        FP += 1.0
      else:
        TP += 1.0
    else:
      # if predicted as not spam when it is then FN
      if row[-1] != 0:
        FN += 1.0
      else:
        TN += 1.0
  #first cutoff everything is not spam
  ROC_TPR = []
  ROC_FPR = []
  tau = sorted(tau, key=lambda row:row[0], reverse = True)
  for i in range(len(tau) + 1):
    TPR = map(lambda row:row[1],tau[0:i]).count(1) / P
    FPR = map(lambda row:row[1],tau[0:i]).count(0) / N
    ROC_TPR.append(TPR)
    ROC_FPR.append(FPR)
  AUC = auc(ROC_FPR, ROC_TPR)
  return [FP, FN, 1 - ((TP + TN) / (P + N)), ROC_TPR, ROC_FPR, AUC]


courses_hash = {}
c1 = "CS5800"
for course in [c1]:#uniq_courses:
	courses_hash[course] = course_label(uniq_courses, course, student_course_map)

means = [ 0.5 for item in  range(len(uniq_courses) + len(frequent_pairs)) ]


student_course_map_c1 = {}
student_course_map_hash = {}
for each in student_course_map:
  if c1 in each[1:]:
    student_course_map_c1[each[0]] = each[1:]
  else:
    student_course_map_hash[each[0]] = each[1:]

# test has all the students eligible this sem with the courses they took
test = AL.create_student_hash(program, cur_sem)
test_list = []
for key in test:
  if key not in student_course_map_c1:
    if key in student_course_map_hash:
      test_list.append([key] + student_course_map_hash[key] + test[key])
    else:

# TEST is wrong. it should have entire history of the student but we keep only courses taken this sem.
test_mapped = course_label(uniq_courses, c1, test)
print map(lambda row:row[-1], test_mapped)

#bayes(courses_hash[c1], means, test_mapped, 0.5)