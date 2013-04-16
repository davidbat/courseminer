import sys
import TotalStudentsPerSem as TSP
import sem_stud_data as SS
from bayes import bayes_mod, predict_bayes
from optparse import OptionParser
import csv
import math
from constants import *

parser = OptionParser()
parser.add_option("-r", "--restrict",
				  action = "store_true", dest="poss_flag", default=False,
                  help="Restrict predictions to courses available for the semester.")
parser.add_option("-s", "--sem",
                  action = "store", dest="cur_sem",
                  help="semester to predict over.")
parser.add_option("-p", "--program",
                  action = "store", dest="program", default= 'MSCS Computer Science',
                  help="program to predict over.\n'MSCS Computer Science' is the default program.")
parser.add_option("-l", "--level",
                  action = "store", dest="level", default= "GR",
                  help="Student level to predict over. Either 'UG' or 'GR'.\n'GR' is the default level")
(options, args) = parser.parse_args()

if args != []:
	print "Too many or too few options specified. Use -h to see usage"
	exit()

def get_frequent_pairs():
	return map(lambda row:row[:-1] ,SS.ReadFile("frequent_pairs.txt", " "))

dont_predict = [ 'CS5010' ]
options = vars(options)
cur_sem = options['cur_sem']
poss_flag = options['poss_flag']
program = options['program'].split(',')
level = options['level']
poss_fn = "stud_actual.txt"
if level == "GR":
	SEM_NUMBER = [ 'sem2', 'sem3', 'sem4' ]
	course_taken = 2.0
else:
	SEM_NUMBER = [ 'sem2', 'sem3', 'sem4', 'sem5', 'sem6', 'sem7']#, 'sem8' ]
	course_taken = 4.0


prior = TSP.calculate_students(cur_sem, level, program)

# false means that we want all prev sems
# true means only cur sem enrolled students
uniq_coursesx, student_course_map = SS.stud_sem_wise_course_map(program, cur_sem, level, False)
uniq_coursesz, student_cur_course_map = SS.stud_sem_wise_course_map(program, cur_sem, level, True)

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
	features = {}
	for sem in SEM_NUMBER:
		features[sem] = {}
	students_last_sem = {}
	for stud_id in student_course_map:
		students_last_sem[stud_id] = find_last_sem(student_course_map[stud_id])
		sem_cnt = 0
		prev_sem_data = student_course_map[stud_id]['sem1']
		for sem in SEM_NUMBER:
			features[sem][stud_id] = map(lambda x:1 if x in prev_sem_data else 0, uniq_courses) + \
				map(lambda courses:1 if courses[0] in prev_sem_data and courses[1] in prev_sem_data else 0, frequent_pairs)
			prev_sem_data += student_course_map[stud_id][sem]

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
	print "Course\t\tActual\tPredict\tDiff\tMSE"
	for key in sorted(predicted_hash):
		actual = 0.0
		if key in actual_hash:
			actual = actual_hash[key]
		if not poss_flag and ((round(predicted_hash[key]) == 0 and actual == 0) 
			or (round(predicted_hash[key]) == 1 and actual == 0)):
			continue
		cnt += 1	
		#else:
		#	continue
		diff = abs(actual - round(predicted_hash[key]))
		mse += diff ** 2
		tabs = '\t'
		if len(key) <= 6:
			tabs += '\t'
		output_str = key + tabs + str(actual) + "\t" + str(round(predicted_hash[key])) + "\t" + \
			str(diff) + "\t" + str(diff ** 2)
		print output_str
		fd.write(output_str + "\n")
	fd.close()
	print "MSE - ", mse / cnt
	print "RMSE - ", math.sqrt(mse / cnt)



course_label_hash = course_label(unique_courses, student_course_map)

poss_courses = unique_courses
actual_courses = {key: float(value) for (key, value) in map(lambda row:row.strip().split(), open(poss_fn).readlines())}
if poss_flag:
	poss_courses = actual_courses.keys()

course_predictor = {} 
course_capacity = {}
means = [ 0.5 for item in range(len(unique_courses+frequent_pairs)) ]
for course in poss_courses:
	if course not in course_label_hash:
		print course, "details not available from previous student history"
		#course_capacity[course] = 0.0
		#dont_predict += [course]
		continue
	course_predictor[course] = {}
	for sem in SEM_NUMBER:
		course_predictor[course][sem] = []
	for sem in SEM_NUMBER:
		course_predictor[course][sem] = bayes_mod(course_label_hash[course][sem], means)


for course in course_predictor:
	course_capacity[course] = 0.0
new_students = 0
predict_over = set(course_capacity.keys()) - set(dont_predict)
for stud_id in student_cur_course_map:
	last_sem = find_last_sem(student_cur_course_map[stud_id])
	# Need random prediction here and for new students
	if last_sem == 'sem1':
		new_students += 1
		continue
	prob = {}
	prev_sem_data = []
	for each_sem in ['sem1'] + SEM_NUMBER[:SEM_NUMBER.index(last_sem)]:
			prev_sem_data += student_cur_course_map[stud_id][each_sem]
	for course in predict_over:
		features = map(lambda x:1 if x in prev_sem_data else 0, unique_courses) + \
			map(lambda courses:1 if courses[0] in prev_sem_data and courses[1] in prev_sem_data else 0, frequent_pairs)
		label = [ 1 if course in student_cur_course_map[stud_id][last_sem] else 0 ]
		prob[course] = predict_bayes(course_predictor[course][last_sem], 
			means, features + label, prior[course])
	Z = sum(map(lambda k:prob[k], prob))
	# stud probably did a course again if he's here
	# or we actually don't have a prediction
	if Z == 0:
		Z = sum(map(lambda k:prior[k], predict_over))
		print stud_id, "don't know what course to give him"
		for course in predict_over:
			course_capacity[course] += course_taken * prior[course] / Z
		continue
	for course in prob:
		course_capacity[course] += course_taken * prob[course] / Z
print "NEW STUDENTS =", new_students
Z = sum(map(lambda k:prior[k], predict_over))

if level == 'GR':
	course_capacity['CS5010'] += new_students
else:
	new_students = new_students * course_taken

for course in predict_over:
	course_capacity[course] += float(new_students) * prior[course] / Z
print "output"
calculate_error(actual_courses, course_capacity)
