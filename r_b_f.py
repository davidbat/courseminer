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

def brute_reenact(prof_course_hash, profs, courses, course_offset, prof_offset):
	first_itr_flag = True
	score = 0
	assign = {}
	second_profs = set([])
	secondary_prof_course_hash = {}
	courses = list(courses[course_offset:] + courses[:course_offset])
	for course in courses:
		offset = 0
		if first_itr_flag == True:
			offset = prof_offset
			first_itr_flag = False
		if len(prof_course_hash[course]) >= offset + 1:
			print course, prof_course_hash[course][offset][0]
			profs -= set([prof_course_hash[course][offset][0]])
			assign[course] = prof_course_hash[course][offset][0]	
			second_profs.union(set([prof_course_hash[course][offset][0]]))
			prof_course_hash, secondary_prof_course_hash = available_prof_hasher(prof_course_hash, profs, secondary_prof_course_hash, second_profs)
		elif len(secondary_prof_course_hash[course]) > 0:
			print course, secondary_prof_course_hash[course][offset][0]
			print "prof -", secondary_prof_course_hash[course][0][0], "assigned twice"
			second_profs -= set([secondary_prof_course_hash[course][0][0]])
			secondary_prof_course_hash, tmp_hash = available_prof_hasher(secondary_prof_course_hash, second_profs, {}, [])
		else:
			print len(courses) - courses.index(course), "courses not assigned"
			print courses[courses.index(course):]
			exit()
		
	return assign


def rec_helper(, min_score):
	for p in profs:
		score, choices = rec(course[c], prof[c][p], c+1)
		if score < min_score:
			min_score = score
			best_choice = choices
	


def reduce_prof_hasher(prof_course_hash, profs):
	tmp_hash = copy.deepcopy(prof_course_hash)
	for course in prof_course_hash:
		tmp_hash[course] = filter(lambda row:row[0] in profs, prof_course_hash[course])
	return tmp_hash

def rec(courses, prof_course_hash, profs, cur_score, cur_choice, min_score, best_choices):
	for c in courses:
		for p in prof_course_hash[courses]:
			choice = copy.deepcopy(cur_choice)
			choice[c] = p[0]
			cur_courses = courses - set([c])
			cur_profs = profs - set([p])
			score, choice = rec(cur_courses, reduce_prof_hasher(prof_course_hash, cur_profs), 
								cur_profs, cur_score + p[1], choice, min_score, best_choices) 
			if score < min_score:
				score = min_score
				best_choices = choice

	return min_score, best_choices



def brute_helper(prof_course_hash, profs, courses, course_offset, prof_offset, trace = False):
	first_itr_flag = True
	score = 0
	second_profs = set([])
	secondary_prof_course_hash = {}
	courses = list(courses[course_offset:] + courses[:course_offset])
	for course in courses:
		offset = 0
		if first_itr_flag == True:
			offset = prof_offset
			first_itr_flag = False
		if len(prof_course_hash[course]) >= offset + 1:
			if trace:
				print course, prof_course_hash[course][offset][0]
			score += prof_course_hash[course][offset][1]
			profs -= set([prof_course_hash[course][offset][0]])
			second_profs.union(set([prof_course_hash[course][offset][0]]))
			prof_course_hash, secondary_prof_course_hash = available_prof_hasher(prof_course_hash, profs, secondary_prof_course_hash, second_profs)
		elif len(secondary_prof_course_hash[course]) > 0:
			#print secondary_prof_course_hash[course]
			if trace:
				print course, prof_course_hash[course][offset][0]
			score += secondary_prof_course_hash[course][0][1] + TWICE_PENALTY
			second_profs -= set([secondary_prof_course_hash[course][0][0]])
			secondary_prof_course_hash, tmp_hash = available_prof_hasher(secondary_prof_course_hash, second_profs, {}, [])
		else:
			# course can't be classified
			#print course
			return float("inf"), [course], courses.index(course)
	return score, [], len(courses)

def most_common(lst, cnt=1):
    return sorted(set(lst), key=lst.count, reverse = True)[:cnt]

def brute_force(prof_course_hash, profs, courses, trace = False):
	assign = {}
	min_score = float("inf")
	best_course_offset = -1
	best_prof_offset = -1
	problem_courses = []
	trace_courses_assigned = 0
	for i in range(len(courses)):
		for j in range(len(prof_course_hash[courses[i]])):
			if trace:
				print "Itr -", courses[i], prof_course_hash[courses[i]][j]
			score, prob_course, courses_assigned = brute_helper(copy.deepcopy(prof_course_hash), set(profs), courses, i, j, trace)
			if trace:
				print "Reuslts -",score, prob_course, courses_assigned, "of", len(courses)
			#print "here:", courses[i], j, score
			#if score != float("inf"):
			#	print "Assigned:"
			#	pprint(brute_reenact(copy.deepcopy(prof_course_hash), set(profs), courses, penalty, i, j))
			if trace and courses_assigned > trace_courses_assigned:
				best_res = i,j
				trace_courses_assigned = courses_assigned
			if score < min_score:
				best_course_offset = i
				best_prof_offset = j
				min_score = score
			elif score == float("inf"):
				problem_courses += prob_course
	if min_score < float("inf"):
		print "min score =", min_score
		brute_reenact(copy.deepcopy(prof_course_hash), set(profs), courses, best_course_offset, best_prof_offset)
	else:
		print "Not Assigned"
		print "Cant allocate course - ", most_common(problem_courses, 2)
		brute_reenact(copy.deepcopy(prof_course_hash), set(profs), courses, best_res[0], best_res[1])
		


def pprint(my_hash):
	for line in my_hash:
		print line,my_hash[line]




available_profs = map(lambda prof:prof.strip(), open("available_profs.txt").readlines())
#print "available_profs" , available_profs
predicted_courses = map(lambda row:row.strip().split()[0], open("Predicted_values.txt").readlines())
#print "predicted_courses", predicted_courses
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
#print "seen_cs_courses", seen_cs_courses
available_profs_course_hash, ignore = available_prof_hasher(course_info, available_profs, {}, [])
#print "available_profs_course_hash", available_profs_course_hash
#brute_force(available_profs_course_hash, available_profs, seen_cs_courses, True)

rec(set(seen_cs_courses), available_profs_course_hash, set(available_profs), 0, {}, float("inf"), {}):

