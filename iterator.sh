if [ $# -eq 0 ]
then
	min_sup="0.3%"
else
	min_sup=$1
fi

cat grad_info.csv | grep -v "Spring 2013" | grep -v "Fall 2012"  > grad_info2.csv

new_stud=`python eligible_student_sem.py "Fall 2012" GR | cut -d " " -f 2`

python pre_proc.py >/dev/null

sh java_run.sh $min_sup > /dev/null

python remap.py CID_hash.txt output.txt > /dev/null

python TotalStudentsPerSem.py "Fall 2012" 

#python test_term.py

python predictor.py $new_stud stud_info.txt 
