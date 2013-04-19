import copy
from collections import Counter

TWICE_PENALTY = 100
# prof_course_hash[course] = [[prof1, rank1], [prof2, rank2]]
def read_courses_prof_hash(prof_course_fn = "courses_professors.txt"):
	with open(prof_course_fn) as fd:
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
		#print prof_course_tmphash
		for course in prof_course_tmphash:
			prof_list = prof_course_tmphash[course]
			tmp_list = map(lambda row:row[0], (sorted(prof_list, key=lambda row:row[1], reverse=True)))
			#print "prof_list", prof_list
			prof_course_hash[course] = map(lambda prof,rank:[prof, rank], tmp_list, range(len(tmp_list)))
			#print prof_course_hash[course]
		return prof_course_hash

def available_prof_hasher(prof_course_hash, profs, secondary_prof_course_hash, second_profs):
	
	for course in prof_course_hash:
		#secondary_prof_course_hash[course] = list(set(secondary_prof_course_hash[course]) + set(filter(lambda row:row[0] in second_profs, prof_course_hash[course])))
		# since only 1 prof at a time
		if course not in secondary_prof_course_hash:
			secondary_prof_course_hash[course] = []
		secondary_prof_course_hash[course] += filter(lambda row:row[0] in second_profs, prof_course_hash[course])
		prof_course_hash[course] = filter(lambda row:row[0] in profs, prof_course_hash[course])
	return prof_course_hash, secondary_prof_course_hash

def reduce_prof_hasher(prof_course_hash, profs):
	tmp_hash = copy.deepcopy(prof_course_hash)
	for course in prof_course_hash:
		tmp_hash[course] = filter(lambda row:row[0] in profs, prof_course_hash[course])
	return tmp_hash

def rec(courses, prof_course_hash, profs, cur_score, cur_choice, min_score, best_choices, cutoff, trace = False, lvl = 0):
	if courses == set([]):
		exit_flag = False
		if cur_score < cutoff:
			exit_flag = True
		return cur_score, cur_choice, exit_flag
	exit_flag = False
	for c in courses:
		if trace:
			print "Course", lvl, c
		for p in prof_course_hash[c]:
			if trace:
				print "Prof", lvl, p
			choice = [c, p[0]]
			cur_courses = courses - set([c])
			cur_profs = profs - set([p[0]])
			score, choice, exit_flag = rec(cur_courses, reduce_prof_hasher(prof_course_hash, cur_profs), 
								cur_profs, cur_score + p[1], cur_choice + choice, min_score, best_choices, cutoff, trace, lvl + 1) 
			if trace:
				print "Score", score, choice
			if score < min_score:
				min_score = score
				best_choices = choice
			if exit_flag:
				break
		if exit_flag:
			break	
	return min_score, best_choices, exit_flag

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
	if course in course_info:
		#print course, " is a new course. We can't schedule it."
	#else:
		seen_cs_courses.append(course)
print "seen_cs_courses", seen_cs_courses
available_profs_course_hash, ignore = available_prof_hasher(course_info, available_profs, {}, [])
print "available_profs_course_hash", available_profs_course_hash
#brute_force(available_profs_course_hash, available_profs, seen_cs_courses, True)

ms, best_choice, flg = rec(set(seen_cs_courses), available_profs_course_hash, set(available_profs), 0, [], float("inf"), {}, len(seen_cs_courses)/2, True, 0)
print "Ended\n", ms, "\n", best_choice

