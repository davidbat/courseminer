import copy
from collections import Counter

TWICE_PENALTY = 100
# prof_course_hash[course] = [[prof1, rank1], [prof2, rank2]]
# Read the professor course hash
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

# Reduce the prof_course_hash to only the current courses and professors
def available_prof_hasher(prof_course_hash, profs, cur_cs_courses):
	tmp_hash = copy.deepcopy(prof_course_hash)
	for course in prof_course_hash:
		if course not in cur_cs_courses:
			tmp_hash.pop(course, None)
		else:
			tmp_hash[course] = filter(lambda row:row[0] in profs, prof_course_hash[course])
	return tmp_hash

# Reduce the prof_course_hash to delete a professor from it
def reduce_prof_hasher(prof_course_hash, profs, c=None):
	tmp_hash = copy.deepcopy(prof_course_hash)
	for course in prof_course_hash:
		if course == c:
			tmp_hash.pop(c)
			continue
		tmp_hash[course] = filter(lambda row:row[0] in profs, prof_course_hash[course])
	return tmp_hash

# First of list
def first(lst):
	if lst == []:
		return None
	else:
		return lst[0]


# The smart recursive function.
# Iterate course by course assigning professors to it.
def smart_rec(courses, prof_course_hash, profs, cur_score, cur_choice, min_score, best_choices, cutoff, trace = False, lvl = 0):
	exit_flag = False
	if len(prof_course_hash) == 0:
		if cur_score < cutoff:
			exit_flag = True
		return cur_score, cur_choice, exit_flag
	
	c = first(sorted(prof_course_hash, key=lambda k:len(prof_course_hash[k])))
	if c != None:
		if trace:
			print "Course", lvl, c, len(prof_course_hash[c])
		for p in prof_course_hash[c]:
			if trace:
				print "Prof", lvl, p
			choice = [[c, p[0]]]
			cur_courses = courses - set([c])
			cur_profs = profs - set([p[0]])
			score, choice, exit_flag = smart_rec(cur_courses, reduce_prof_hasher(prof_course_hash, cur_profs, c), 
								cur_profs, cur_score + p[1], cur_choice + choice, min_score, best_choices, cutoff, trace, lvl + 1) 
			if trace:
				print "Score", score, choice, exit_flag
			if score < min_score:
				min_score = score
				best_choices = choice
			if exit_flag:
				break
	return min_score, best_choices, exit_flag

def pprint(my_hash):
	for line in my_hash:
		print line,my_hash[line]

def sprint(my_hash):
	for line in my_hash:
		print line[0], line[1]


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
		seen_cs_courses.append(course)
		
#print "seen_cs_courses", seen_cs_courses
#print len(course_info)
available_profs_course_hash = available_prof_hasher(course_info, available_profs, seen_cs_courses)
#print "available_profs_course_hash", available_profs_course_hash
#brute_force(available_profs_course_hash, available_profs, seen_cs_courses, True)
#print len(available_profs_course_hash)
ms, best_choice, flg = smart_rec(set(seen_cs_courses), available_profs_course_hash, set(available_profs), 0, [], float("inf"), {}, len(seen_cs_courses)/2, False, 0)
print "Ended with a score - ", ms, "\n"
sprint(best_choice)

