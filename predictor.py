import sys

# replaces multiple occurances of course in out[0..1] with 1 occurance. If the occurance
# is originally only 1, then it deletes it from the list.
def replace_mult(out, course):
	for item in out:
		new_item = filter(lambda x:x != course, item)
		if item.count(course) > 1:
			item = [course] + new_item
		else:
			# 1 or zero occurance
			item = new_item
	return out

def ReadFile(fn):
	features = []
	for line in open(fn).readlines():
		features.append(map(lambda i: i, line.split()))
	return features

def random_prediction(possible_courses, course_hash, out, n):
	prob = []
	#course_hash = {}
	for item in out:
		if len(item) == 2 and item[0] != 'CS5010':
			#print item[1]
			prob.append(item)

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


def calculate_error(actual_hash, predicted_hash):
	mse = 0
	cnt = 0
	for key in predicted_hash:
		actual = 0
		if key in actual_hash:
			actual = actual_hash[key]
			cnt += 1
		else:
			continue
		diff = abs(actual - round(predicted_hash[key]))
		mse += diff ** 2
		print key, actual, round(predicted_hash[key]), \
			diff, diff ** 2
	print "MSE - ", mse / (cnt * 2)



fp = ReadFile("final.txt")
poss_flag = False
ar = 0
if sys.argv[1] == "-p":
	ar = 1
	poss_flag = True
new_students = float(sys.argv[ar+1])
student_course_info = ReadFile(sys.argv[ar+2])
possible_courses = []
if poss_flag: possible_courses = map(lambda st:st[:-1], open(sys.argv[ar+3]).readlines())
course_hash = {} 
randoms = 0
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

	prob = []
	for item in out:
		if len(item) == 2 and item[0] != 'CS5010':
			#print item
			prob.append(item)


	random_prediction(possible_courses, course_hash, out, 2)


course_hash['CS5010'] = new_students
out = list(fp)
random_prediction(possible_courses, course_hash, out, new_students)

csum = 0 
for key in course_hash:
	#print key, " - ", course_hash[key]
	csum += course_hash[key]

actual_hash = {}
for line in ReadFile('./data/stud_spring_actual.txt'):
	#print line
	if line[0] in actual_hash:
		actual_hash[line[0]] += float(line[1])
	else:
		actual_hash[line[0]] = float(line[1])
calculate_error(actual_hash, course_hash)
print "Total sum of courses taken - ",  csum
