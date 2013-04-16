import sys
import math

# Read file into hash
def ReadFile(fn):
	features = []
	for line in open(fn).readlines():
		features.append(map(lambda i: i, line.split()))
	return features


# Compile a probability distibution for all courses based on 'out' and save it in course_hash.
# This is run for a student. 
# Probabilities are smoother by 'smoothing_const'
# Courses that are in my_courses are ignored (as they have already been taken)
def random_prediction(my_courses, all_courses, possible_courses, course_hash, out, n, poss_flag, level = 'GR'):
	smoothing_const = 0.1
	unwanted_cids = [ 	'CS1210', 'CS1501', 'CS1801', 'CS2501', 'CS2511', 'CS2801', 'CS2900', 'CS2901', 
						'CS4611', 'CS4991', 'CS4993', 'CS5011', 'CS5336', 'CS6949', 'CS7381', 'CS7990', 
						'CS7996', 'CS8674', 'CS8949', 'CS8982', 'CS8984', 'CS8986', 'CS9990', 'CS9996', 
						'IA5131', 'IA5151', 'IA5211', 'IA5978', 'IA5984', 'IA8982', 'CS6964',
						'BUSN1100','COOP3945','CS1210','CS1220','CS6949','CS6964','MATH3000','MATH4000' ]
	if level == 'GR':
		unwanted_cids += [ 'CS5010' ]
	prob_hash = {}
	for course in all_courses:
		prob_hash[course] = smoothing_const
	for item in out:
		if len(item) == 2 and item[0] not in unwanted_cids and item[0] not in my_courses:
			prob_hash[item[0]] += int(item[1])

	prob = map(lambda k:[k,prob_hash[k]],prob_hash)

	not_required = []
	if poss_flag: not_required = list(set(map(lambda x:x[0], prob)) - set(possible_courses))
	prob = filter(lambda x: x[0] not in not_required, prob)
	if poss_flag and len(prob) > len(possible_courses): print "Something wrong, courses went over possible list"
	my_sum = sum(map(lambda x:float(x[1]),prob))
	for item in prob:
		if not course_hash.has_key(item[0]):
				course_hash[item[0]] = 0
		course_hash[item[0]] += n * (float(item[1])/my_sum)


# calculate error will calculate the MSE between the number of students
# that actually took a course and the predicted value.
def calculate_error(actual_hash, predicted_hash, poss_flag):
	mse = 0
	cnt = 0
	fd = open("Predicted_values.txt", "w")
	print "Course\t\tActual\tPredict\tDiff\tMSE"
	for key in sorted(predicted_hash):
		actual = 0.0
		if key in actual_hash:
			actual = actual_hash[key]
		if not poss_flag and (round(predicted_hash[key]) == 0 and actual == 0) or (round(predicted_hash[key]) == 1 and actual == 0):
			continue
		cnt += 1
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


# main does the actual predicting. It iterates over every student in the current semester,
# and calculates the probabilities that the student takes various courses.
# The calcualted probabilities are saved into course_hash
def main(new_students, level = 'GR', poss_flag = False, student_course_info_fn = "stud_info.txt"):
	if level == 'GR':
		courses_taken = 2.0
	else:
		courses_taken = 4.0
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
		out = list(fp)
		for course in courses:
			out	= [ filter(lambda x:x != course, item) for item in out if item.count(course) > 0 ]
			out	= [ item for item in out if len(item) > 1 ]
		
		if len(out) < 1:
			out = list(fp)
			for course in courses:
				out	= filter(lambda x:x != course, out)
				out	= [ item for item in out if len(item) > 1 ]

		random_prediction(courses, all_courses, possible_courses, course_hash, out, courses_taken, poss_flag, level)

	if level == 'GR':
		# CS5010 is PDP is a special case. All GR new students must take it.
		course_hash['CS5010'] = new_students
	else:
		new_students *= courses_taken
	out = list(fp)
	random_prediction([], all_courses, possible_courses, course_hash, out, new_students, poss_flag, level)

	csum = 0 
	for key in course_hash:
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
