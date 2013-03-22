cd '/home/dave/Dropbox/my stuff/dm/courseminer/selenium'
pwd
cat sems | while read sem
do
	for i in 1 2 3 4 5 6 7 8 9
	do
		echo $sem, $i 
		python all_courses.py $i `echo $sems | tr -d "\n"`
		killall firefox
		if [ $? -ne 0 ]
		then
			echo $sem $i had a problem
		fi
	done
done
