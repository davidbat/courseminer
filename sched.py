import copy

# prof_course_hash[course] = [[prof1, rank1], [prof2, rank2]]
def read_courses_prof_hash(prof_course_fn = "courses_professors.txt"):
	with open(prof_course_fn) as fd:
		penalty = 100
		prof_course_tmphash = {}
		for line in fd.readlines():
			line = line.strip().split()
			prof = " ".join(line [1:3])
			count = line [3]
			course = line [0]
			if course in prof_course_tmphash:
				prof_course_tmphash[course].append([prof, count])
			else:
				prof_course_tmphash[course] = [[prof, count]]

		prof_course_hash = {}
		rank = {}
		print prof_course_tmphash
		for course in prof_course_tmphash:
			prof_list = prof_course_tmphash[course]
			tmp_list = map(lambda row:row[0], (sorted(prof_list, key=lambda row:row[1], reverse=True)))
			#print "prof_list", prof_list
			prof_course_hash[course] = map(lambda prof,rank:[prof, rank], tmp_list, range(len(tmp_list)))
			#print prof_course_hash[course]
		return prof_course_hash

def available_prof_hasher(prof_course_hash, profs):
	for course in prof_course_hash:
		prof_course_hash[course] = filter(lambda row:row[0] in profs, prof_course_hash[course])
	return prof_course_hash

def brute_reenact(prof_course_hash, profs, courses, penalty, course_offset, prof_offset):
	first_itr_flag = True
	score = 0
	assign = {}
	for course in courses[course_offset:] + courses[:course_offset]:
		offset = 0
		if first_itr_flag == True:
			offset = prof_offset
			first_itr_flag = False
		assign[course] = prof_course_hash[course][offset][0]
		profs -= set([prof_course_hash[course][offset][0]])
		prof_course_hash = available_prof_hasher(prof_course_hash, profs)
	return assign

def brute_helper(prof_course_hash, profs, courses, penalty, course_offset, prof_offset):
	first_itr_flag = True
	score = 0
	for course in courses[course_offset:] + courses[:course_offset]:
		offset = 0
		if first_itr_flag == True:
			offset = prof_offset
			first_itr_flag = False
		if len(prof_course_hash[course]) >= offset + 1:
			score += prof_course_hash[course][offset][1]
			profs -= set([prof_course_hash[course][offset][0]])
			prof_course_hash = available_prof_hasher(prof_course_hash, profs)
		else:
			# course can't be classified
			print course
			return float("inf")
	return score

def brute_force(prof_course_hash, profs, courses, penalty = 100):
	assign = {}
	min_score = float("inf")
	best_course_offset = -1
	best_prof_offset = -1
	for i in range(len(courses)):
		for j in range(len(prof_course_hash[courses[i]])):
			score = brute_helper(copy.deepcopy(prof_course_hash), set(profs), courses, penalty, i, j)
			print "here:", courses[i], j, score
			#if score != float("inf"):
			#	print "Assigned:"
			#	pprint(brute_reenact(copy.deepcopy(prof_course_hash), set(profs), courses, penalty, i, j))
			if score < min_score:
				best_course_offset = i
				best_prof_offset = j
				min_score = score
	if min_score < float("inf"):
		return brute_reenact(copy.deepcopy(prof_course_hash), set(profs), courses, penalty, best_course_offset, best_prof_offset)
	else:
		return {}

def pprint(my_hash):
	for line in my_hash:
		print line,my_hash[line]




available_profs = map(lambda prof:prof.strip(), open("available_profs.txt").readlines())
print "available_profs" , available_profs
predicted_courses = map(lambda row:row.strip().split()[0], open("Predicted_values.txt").readlines())
print "predicted_courses", predicted_courses
all_cs_courses = map(lambda prof:prof.strip(), open("ccis_courses.txt").readlines())
non_cs_courses = set(predicted_courses) - set(all_cs_courses)
predicted_cs_courses = list(set(predicted_courses) - non_cs_courses)
course_info = read_courses_prof_hash()

seen_cs_courses = []
for course in predicted_cs_courses:
	if course not in course_info:
		print course, " is a new course. We can't schedule it."
	else:
		seen_cs_courses.append(course)
print "seen_cs_courses", seen_cs_courses
available_profs_course_hash = available_prof_hasher(course_info, available_profs)
#print "available_profs_course_hash", available_profs_course_hash
assigned_courses = brute_force(available_profs_course_hash, available_profs, seen_cs_courses)

if assigned_courses == {}:
	# we have to redo deleting a course?
	# delete smallest course
	print "Oops"
else:
	print "Assigned"
	pprint(assigned_courses)
