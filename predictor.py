import sys
import math
def ReadFile(fn):
	features = []
	for line in open(fn).readlines():
		features.append(map(lambda i: i, line.split()))
	return features


# We can remove my_courses or set it to empty because it increases MSE (Spring 2013)
def random_prediction(my_courses, all_courses, possible_courses, course_hash, out, n, poss_flag, level = 'GR'):
	smoothing_const = 0.1
	unwanted_cids = ['CS6949', 'CS6964', 'CS5011', 'BUSN1100','COOP3945',
			'CS1210','CS1220','CS6949','CS6964','MATH3000','MATH4000' ]
	if level == 'GR':
		# add pdp
		unwanted_cids += [ 'CS5010' ]
	prob_hash = {}
	for course in all_courses:
		prob_hash[course] = smoothing_const
	#course_hash = {}
	for item in out:
		if len(item) == 2 and item[0] not in unwanted_cids and item[0] not in my_courses:
			#print item[1]
			prob_hash[item[0]] += int(item[1])

	prob = map(lambda k:[k,prob_hash[k]],prob_hash)

	not_required = []
	if poss_flag: not_required = list(set(map(lambda x:x[0], prob)) - set(possible_courses))
	prob = filter(lambda x: x[0] not in not_required, prob)
	if poss_flag and len(prob) > len(possible_courses): print "Something wrong, courses went over possible list"
	my_sum = sum(map(lambda x:float(x[1]),prob))
	for item in prob:
		if not course_hash.has_key(item[0]):
				#print item[0]
				course_hash[item[0]] = 0
		course_hash[item[0]] += n * (float(item[1])/my_sum)


def calculate_error(actual_hash, predicted_hash, poss_flag):
	mse = 0
	cnt = 0
	fd = open("Predicted_values.txt", "w")
	print "Course\tActual\tPredict\tDiff\tMSE"
	for key in sorted(predicted_hash):
		actual = 0.0
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
	print "MSE - ", mse / cnt	
	print "RMSE - ", math.sqrt(mse / cnt)

def main(new_students, level = 'GR', poss_flag = False, student_course_info_fn = "stud_info.txt"):
	#print "pss = ", poss_flag
	if level == 'GR':
		courses_taken = 2.0
	else:
		courses_taken = 4.0
	#print courses_taken
	student_course_info = ReadFile(student_course_info_fn)
	fp = ReadFile("final.txt")
	all_courses = map(lambda row:row[1], ReadFile("CID_hash.txt"))
	possible_courses = []
	poss_fn = "stud_actual.txt"
	actual_hash = {key: float(value) for (key, value) in map(lambda row:row.strip().split(), open(poss_fn).readlines())}
	if poss_flag:
		possible_courses = actual_hash.keys()
	course_hash = {} 
	for courses in student_course_info:
		#print courses
		out = list(fp)
		for course in courses:
			# Replace mult works but screws up probabilities completely and takes too long. So don't use it
			out	= [ filter(lambda x:x != course, item) for item in out if item.count(course) > 0 ]
			out	= [ item for item in out if len(item) > 1 ]
		
		if len(out) < 1:
			out = list(fp)
			for course in courses:
				out	= filter(lambda x:x != course, out)
				out	= [ item for item in out if len(item) > 1 ]


		# NOTE TO SOME :-
		# Code handles multiple occurances of a course by replacing all of them with ''. Gotta replace 3 with 2 and
		# not ''

		random_prediction(courses, all_courses, possible_courses, course_hash, out, courses_taken, poss_flag, level)

	if level == 'GR':
		course_hash['CS5010'] = new_students
	else:
		new_students *= courses_taken
	out = list(fp)
	random_prediction([], all_courses, possible_courses, course_hash, out, new_students, poss_flag, level)

	csum = 0 
	for key in course_hash:
		#print key, " - ", course_hash[key]
		csum += course_hash[key]

	calculate_error(actual_hash, course_hash, poss_flag)
	print "Total sum of courses taken - ",  csum

if __name__ == "__main__":
	poss_flag = False
	ar = 0
	if sys.argv[1] == "-p":
		ar = 1
		poss_flag = True
	level = sys.argv[ar+1]
	new_students = float(sys.argv[ar+2])
	student_course_info_fn = sys.argv[ar+3]
	print level, new_students, student_course_info_fn
	main(new_students, level, poss_flag, student_course_info_fn)
