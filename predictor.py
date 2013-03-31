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
	# dont normalize because gaussian gets worse
	#for index in range(len(features[0]) - 1):
	#  col = normList(map(lambda row:row[index], features))
	#  for f in range(len(features)):
	#    features[f][index] = col[f]
	return features

def random_prediction(possible_courses, course_hash, out, n):
	prob = []
	#course_hash = {}
	for item in out:
		if len(item) == 2 and item[0] != 'CS5010':
			#print item[1]
			prob.append(item)

	not_required = []
	if poss_flag == True: not_required = list(set(map(lambda x:x[0], prob)) - set(possible_courses))
	prob = filter(lambda x: x[0] not in not_required, prob)
	my_sum = sum(map(lambda x:float(x[1]),prob))
	if poss_flag and len(prob) > len(possible_courses): print len(prob)
	for item in prob:
		if not course_hash.has_key(item[0]):
				#print item[0]
				course_hash[item[0]] = 0
		course_hash[item[0]] += n * (float(item[1])/my_sum)



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
		#out = replace_mult(out, course)
		out	= [ filter(lambda x:x != course, item) for item in out if item.count(course) > 0 ]
		out	= [ item for item in out if len(item) > 1 ]

		#print out
	#tmp_out	= [ item for item in out if item.count(course) == 1 ]
	#tmp_out_2 = [ filter(lambda x:x != course, item) for item in out if item.count(course) > 1 ]
	#out = tmp_out + tmp_out_2
		#out = [ item for item in out if item.count(course) > 0 ]
		#print out
		#for each in out:		
		#	each = filter(lambda row:row!=course, each)
	#print courses
	# have to remove courses from out below -
	if len(out) < 2:
		out = list (fp)

	# NOTE TO SOME :-
	# Man I'm tired now. The above line is totally hacked in. Doesn't work for [['7'], ['4']]
	# Code handles multiple occurances of a course by replacing all of them with ''. Gotta replace 3 with 2 and
	# not ''


	#dont_want = []# ['CS6949', 'CS6964']

	prob = []
	for item in out:
		if len(item) == 2 and item[0] != 'CS5010':
			#print item
			prob.append(item)

	not_required = []
	if poss_flag: not_required = list(set(map(lambda x:x[0], prob)) - set(possible_courses))
	prob = filter(lambda x: x[0] not in not_required, prob)
	if poss_flag and len(prob) > len(possible_courses): print "Something wrong, courses went over possible list"
	my_sum = sum(map(lambda x:float(x[1]),prob))

	temp_sum = 0
	for item in prob:
		#print item
		if not course_hash.has_key(item[0]):
			#print item[0]
			course_hash[item[0]] = 0
		course_hash[item[0]] += ( 2 * float(item[1])/my_sum )
		temp_sum += 2 * float(item[1])/my_sum

	#print temp_sum
	if temp_sum == 0 :
		randoms += 1
		#print "Should not be here"
		#print out
#if not course_hash.has_key('CS5010'):
#	course_hash['CS5010'] = 0
course_hash['CS5010'] = new_students
print "Could not find information for ", randoms, " students"
out = list(fp)
random_prediction(possible_courses, course_hash, out, new_students + randoms * 2)
#out = [ item for item in out if item.count(course) > 0 ]
#print out

#csum = 0 
#for key in course_hash:
#	print key, " - ", course_hash[key]
#	csum += course_hash[key]

#print sum

#for line in out:
	#print " ".join(line)
#	print " ".join(filter(lambda x:x not in dont_want,line))

#print "\n\n"
csum = 0 
for key in course_hash:
	print key, " - ", course_hash[key]
	csum += course_hash[key]
print "Total sum of courses taken - ",  csum
