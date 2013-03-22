for i in `cat folders`
do
	for j in 1 2 3 4 5 6 7 8 9
	do
		grep -c Instructors $i/$j
		if [ `grep -c Instructors $i/$j` -eq 0 ]
		then
			echo $i $j
		fi
	done
done
