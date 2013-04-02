

if [ $# -lt 1 ]
then
	echo Need to supply semester
	exit
fi
cur_sem=$1
if [ $# -eq 1 ]
then
	min_sup="0.3%"
else
	min_sup=$2
fi
echo $cur_sem
my_set=`python find_sems.py "$cur_sem"`
echo $my_set
cat grad_info.csv | egrep -v "$my_set"  > grad_info2.csv

new_stud=`python eligible_student_sem.py "$cur_sem" GR | cut -d " " -f 2`

echo $new_stud new students
echo `wc -l eligible_stud.txt` eligible students from previous semesters
python pre_proc.py >/dev/null

sh java_run.sh $min_sup > /dev/null

python remap.py CID_hash.txt output.txt > /dev/null

python TotalStudentsPerSem.py "$cur_sem" 

#python test_term.py

python predictor.py $new_stud stud_info.txt 
