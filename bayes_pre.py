import sys
import TotalStudentsPerSem as TSP
import pre_proc as PP
import csv
import eligible_student_sem as ES
import actual_labels as AL
import math
import sem_stud_data as SS
from bayes import bayes

def get_frequent_pairs():
	return map(lambda row:row[:-1] ,SS.ReadFile("frequent_pairs.txt", " "))

DUMMY = 999
cur_sem = sys.argv[1]

program = [ 'MSCS Computer Science' ]
if len(sys.argv) > 2:
	program = sys.argv[2:]

TSP.calculate_students(cur_sem, program)


uniq_coursesx, student_course_map = SS.stud_sem_wise_course_map(program, cur_sem, "Graduate", False)
uniq_coursesz, student_cur_course_map = SS.stud_sem_wise_course_map(program, cur_sem, "Graduate", True)

unique_courses = list(set(uniq_coursesx + uniq_coursesz))

frequent_pairs = get_frequent_pairs()


def pprint(my_hash):
	for line in my_hash:
		print line

def course_label(uniq_courses, student_course_map):
	course_label_hash = {}
	features = { 'sem2':{}, 'sem3':{}, 'sem4':{} }
	for stud_id in student_course_map:
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
		for sem in [ 'sem2', 'sem3', 'sem4']:
			course_label_hash[course][sem] = []
			for stud_id in student_course_map:
				sem_data = student_course_map[stud_id][sem]
				course_label_hash[course][sem].append(features[sem][stud_id] + [ 1 if course in sem_data else 0 ])
			 
	#pprint (course_label_hash['CS5610']['sem2'])
	return course_label_hash


course_label_hash = course_label(unique_courses, student_course_map)
test = course_label(unique_courses,student_cur_course_map)

for course in unique_courses:
	means = [ 0.5 for item in range(len(course_label_hash[course]['sem4'][0]) -1) ]
	FP, FN, ERR, ROC_TPR, ROC_FPR, AUC = bayes(course_label_hash[course]['sem4'], means, test[course]['sem4'], 0.5)
	print course ," ->  error = ", ERR, "\t\tAUC = ", AUC

