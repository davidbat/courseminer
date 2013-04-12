import sys
import TotalStudentsPerSem as TSP
import pre_proc as PP
import csv
import eligible_student_sem as ES
import actual_labels as AL
import math
import sem_stud_data as SS
from bayes import bayes, bayes_mod, predict_bayes

def get_frequent_pairs():
	return map(lambda row:row[:-1] ,SS.ReadFile("frequent_pairs.txt", " "))

SEM_NUMBER = [ 'sem2', 'sem3', 'sem4' ]

DUMMY = 999
poss_flag = False
opt = 0
if sys.argv[1] == "-p":
	opt = 2
	poss_fn = sys.argv[2]
	poss_flag = True
new_students = sys.argv[opt+1]
cur_sem = sys.argv[opt+2]

program = [ 'MSCS Computer Science' ]
if len(sys.argv) > opt+3:
	program = sys.argv[opt+3:]

prior = TSP.calculate_students(cur_sem, program)
print "prior =", prior['CS5800']
# false means that we want all prev sems
# true means only cur sem enrolled students
uniq_coursesx, student_course_map = SS.stud_sem_wise_course_map(program, cur_sem, "Graduate", False)
uniq_coursesz, student_cur_course_map = SS.stud_sem_wise_course_map(program, cur_sem, "Graduate", True)

unique_courses = list(set(uniq_coursesx + uniq_coursesz))

frequent_pairs = get_frequent_pairs()


def pprint(my_hash):
	for line in my_hash:
		print line,my_hash[line]

def find_last_sem(sem_hash):
	sems = sorted(sem_hash)
	for indx in range(len(sems)):
		if sem_hash[sems[indx]] == []:
			return sems[indx-1]
	return sems[-1]

def course_label(uniq_courses, student_course_map, test_flag=False):
	course_label_hash = {}
	features = { 'sem2':{}, 'sem3':{}, 'sem4':{} }
	students_last_sem = {}
	for stud_id in student_course_map:
		students_last_sem[stud_id] = find_last_sem(student_course_map[stud_id])
		sem1 = student_course_map[stud_id]['sem1']
		sem2 = student_course_map[stud_id]['sem2']
		sem3 = student_course_map[stud_id]['sem3']
		sem4 = student_course_map[stud_id]['sem4']
		features['sem2'][stud_id] = map(lambda x:1 if x in sem1 else 0, uniq_courses) + \
			map(lambda courses:1 if courses[0] in sem1 and courses[1] in sem1 else 0, frequent_pairs)
		features['sem3'][stud_id] = map(lambda x:1 if x in sem1+sem2 else 0, uniq_courses) + \
			map(lambda courses:1 if courses[0] in sem1+sem2 and courses[1] in sem1 else 0, frequent_pairs)
		features['sem4'][stud_id] = map(lambda x:1 if x in sem1+sem2+sem3 else 0, uniq_courses) + \
			map(lambda courses:1 if courses[0] in sem1+sem2+sem3 and courses[1] in sem1 else 0, frequent_pairs)


	for course in uniq_courses:
		course_label_hash[course] = {}
		for sem in SEM_NUMBER:
			course_label_hash[course][sem] = []
			for stud_id in student_course_map:
				if test_flag and students_last_sem[stud_id] != sem:
					continue
				sem_data = student_course_map[stud_id][sem]
				# Student hasn't taken courses for this sem or ahead. Don't consider him
				if sem_data == []:
					continue
				course_label_hash[course][sem].append(features[sem][stud_id] + [ 1 if course in sem_data else 0 ])

	#pprint (course_label_hash['CS5610']['sem2'])
	return course_label_hash


def calculate_error(actual_hash, predicted_hash):
	mse = 0
	cnt = 0
	fd = open("Predicted_values.txt", "w")
	print "Course\tActual\tPredict\tDiff\tMSE"
	for key in predicted_hash:
		actual = 0
		if key in actual_hash:
			actual = actual_hash[key]
		if not poss_flag and (round(predicted_hash[key]) == 0 and actual == 0) or (round(predicted_hash[key]) == 1 and actual == 0):
			continue
		cnt += 1	
		#else:
		#	continue
		diff = abs(actual - round(predicted_hash[key]))
		mse += diff ** 2
		output_str = key + "\t" + str(actual) + "\t" + str(round(predicted_hash[key])) + "\t" + \
			str(diff) + "\t" + str(diff ** 2)
		print output_str
		fd.write(output_str + "\n")
	fd.close()
	print "MSE - ", mse / (cnt * 2)



course_label_hash = course_label(unique_courses, student_course_map)
#test = course_label(unique_courses,student_cur_course_map, True)

poss_courses = unique_courses
if poss_flag:
	poss_courses = map(lambda row:row.strip(), open(poss_fn).readlines())
	print poss_courses

course_predictor = {} 
means = [ 0.5 for item in range(len(unique_courses+frequent_pairs)) ]
for course in poss_courses:
	if course not in course_label_hash:
		print course, " not available"
		continue
	course_predictor[course] = { 'sem2':[], 'sem3':[], 'sem4':[] }
	for sem in SEM_NUMBER:

		course_predictor[course][sem] = bayes_mod(course_label_hash[course][sem], means)
		#FP, FN, P, N, ERR, ROC_TPR, ROC_FPR, AUC = bayes_mod(course_label_hash[course][sem], means, test[course][sem], 0.5)
		#print course ," ->  error = %.2f" % ERR, "\tAUC = %.2f" % AUC, "\tFP = %.2f" % FP, "\tFN = %.2f" % FN, "\tP = ", P, "\tN = ", N

course_capacity = {}
for course in course_predictor:
	course_capacity[course] = 0.0

for stud_id in student_cur_course_map:
	last_sem = find_last_sem(student_cur_course_map[stud_id])
	# Need random prediction here and for new students
	if last_sem == 'sem1':
		continue
	prob = {}
	prev_sem_data = []
	for each_sem in ['sem1'] + SEM_NUMBER[:SEM_NUMBER.index(last_sem)]:
			prev_sem_data += student_cur_course_map[stud_id][each_sem]
	for course in course_predictor:
		features = map(lambda x:1 if x in prev_sem_data else 0, unique_courses) + \
			map(lambda courses:1 if courses[0] in prev_sem_data and courses[1] in prev_sem_data else 0, frequent_pairs)
		label = [ 1 if course in student_cur_course_map[stud_id][last_sem] else 0 ]
		
		prob[course] = predict_bayes(course_predictor[course][last_sem], 
			means, features + label, prior[course])
	print stud_id, student_cur_course_map[stud_id], prev_sem_data
	pprint(prob)
	Z = sum(map(lambda k:prob[k], prob))
	# stud probably did a course again if he's here
	# or we actually don't have a prediction
	if Z == 0:
		Z = sum(map(lambda k:prior[k], course_capacity))
		print stud_id, "don't know what course to give him"
		for course in course_capacity:
			course_capacity[course] += 2.0 * prior[course] / Z
		continue
	for course in prob:
		course_capacity[course] += 2 * prob[course] / Z
Z = sum(map(lambda k:prior[k], course_capacity))
for course in course_capacity:
	course_capacity[course] += float(new_students) * prior[course] / Z
print "output"
pprint(course_capacity)