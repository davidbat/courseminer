import sys

cur_sem = sys.argv[1]

sems = ['Fall 2009', 'Spring 2010', 'Fall 2010', 'Spring 2011', 'Fall 2011', 'Spring 2012', 'Fall 2012', 'Spring 2013']

indx = sems.index(cur_sem)

print "|".join(sems[indx:])
