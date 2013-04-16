import sys

# Return a pipe seperated list of previous semesters
def find_sems(cur_sem):
	sems = ['Fall 2009', 'Spring 2010', 'Fall 2010', 'Spring 2011', 'Fall 2011', 'Spring 2012', 'Fall 2012', 'Spring 2013']
	indx = sems.index(cur_sem)
	return "|".join(sems[indx:])

if __name__ == "__main__":
	cur_sem = sys.argv[1]
	print find_sems(cur_sem)
