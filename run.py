from optparse import OptionParser
import os
import find_sems as FS
import subprocess as sub
import eligible_student_sem as ESS
import pre_proc as PP
import TotalStudentsPerSem as TSP
import predictor as Pred

parser = OptionParser()
parser.add_option("-r", "--restrict",
				  action = "store_true", dest="poss_flag", default=False,
                  help="Restrict predictions to courses available for the semester.")
parser.add_option("-s", "--sem",
                  action = "store", dest="cur_sem",
                  help="semester to predict over.")
parser.add_option("-p", "--program",
                  action = "store", dest="program", default= 'MSCS Computer Science',
                  help="programs to predict over. They should be comma seperated single string, no extra spaces\
                  	\n'MSCS Computer Science' is the default program.")
parser.add_option("-l", "--level",
                  action = "store", dest="level", default= "GR",
                  help="Student level to predict over. Either 'UG' or 'GR'.\n'GR' is the default level")
parser.add_option("-m", "--minsup",
                  action = "store", dest="min_sup", default= "0.3",
                  help="The minimum support to consider for Frequent Patters. 0.3 is the default value")
(options, args) = parser.parse_args()

#print options
if args != []:
	print "Too many or too few options specified. Use -h to see usage"
	exit()


options = vars(options)
cur_sem = options['cur_sem']
poss_flag = options['poss_flag']
program = options['program'].split(',')
level = options['level']
min_sup = options['min_sup']
poss_fn = "stud_actual.txt"

if level == "UG" and float(min_sup) < 2.0:
	print "Changing min_sup to 2.0 for performance"
	min_sup = "2.0"

my_set = FS.find_sems(cur_sem)
#print 'cat CourseEnrollmentInfo.csv | grep ' + level + ' | egrep -v "' + my_set + '"  > grad_info2.csv'

os.system('cat CourseEnrollmentInfo.csv | grep ' + level + ' | egrep -v "' + my_set + '"  > grad_info2.csv')

old_students, new_students = ESS.number_new_studs(cur_sem, level, program)

print str(new_students) + " new students"
print str(old_students) + " students eligible from previous semesters"
PP.create_common_id(program)

os.system("sh java_run.sh " + min_sup + "%> /dev/null")

os.system("python remap.py CID_hash.txt output.txt > /dev/null")

TSP.calculate_students(cur_sem, level, program)
#print float(new_students), level, poss_flag
Pred.main(float(new_students), level, poss_flag)
