import copy





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



def pprint(my_hash):
	for line in my_hash:
		print line,my_hash[line]



def cluster(profs_course_hash):
	clusters = {}
	clustered = []
	for course in profs_course_hash:
		flag = False
		if course not in clustered:
			profs = set(map(lambda row:row[0], profs_course_hash[course]))
			for c in clusters:
				if clusters[c]['profs'].intersection(profs) == set([]):
					continue
				#print c, course, "here"
				#print "b4", clusters[c]['courses']
				clusters[c]['courses'] = clusters[c]['courses'].union(set([course]))
				#print "aft", clusters[c]['courses']
				clusters[c]['profs'] = clusters[c]['profs'].union(profs)
				clustered.append(course)
				flag = True
				break
			if not flag:
				clusters[course] = {}
				clusters[course]['courses'] = set([course])
				clusters[course]['profs'] = profs
	print len(clusters)
	print len(clustered), clustered
	pprint(clusters)
	return clusters


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
cluster(available_profs_course_hash)
