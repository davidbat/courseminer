import sys

# convert the ids in the courses taken from my_ids to actual CCIS ids
def rehash(hs, ls):
	out = open("final.txt", "w")
	for each in ls:
		tmp_ls = []
		for mid in each[:-1]:
			#print mid
			tmp_ls.append(hs[mid])
		tmp_ls.append(each[-1])
		out.write(" ".join(tmp_ls) + "\n")
	out.close()

# Read the course id hash from file
def readhash(fn):
	fd = open(fn)
	my_hash = {}
	for line in fd.readlines():
		mid, cid = line.split()
		#print mid, "a", cid
		my_hash[mid] = cid
	return my_hash

# read the courses taken from files into a list
def readlist(fn): 
	fd = open(fn)
	my_list = []
	for line in fd.readlines():
		my_list.append("".join(map(lambda ch: ch if ch != ":" else " ", line.strip())).split())
	#print my_list
	return my_list

Usage = "python remap.py <hash> <file to remap>"
if len(sys.argv) != 3:
	print "Incorrect number of arguments given."
	print Usage
else:
	cid_hash = readhash(sys.argv[1])
	to_remap = readlist(sys.argv[2])
	rehash(cid_hash, to_remap)