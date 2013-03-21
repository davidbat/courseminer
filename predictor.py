import sys

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

fp = ReadFile("final.txt")
out = list(fp)
for course in sys.argv[1:]:
	#out	= [ filter(lambda x:x != course, item) for item in out if item.count(course) > 0 ]
	out = [ item for item in out if item.count(course) > 0 ]

dont_want = ['CS6949', 'CS6964']
for line in out:
	print " ".join(line)
	#print " ".join(filter(lambda x:x not in dont_want,line))