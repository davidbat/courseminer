#!/bin/bash

python parser.v5.py
#python TotalStudentsPerSem.py 
cat *.out | sort -u > all_classes.csv
rm ./missing_courses.csv
cat uniq_missing |while read i; do crn=`echo $i  | cut -d " " -f 1`; course=`echo $i | cut -d " " -f 2,3`; ln=`grep $crn all_classes.csv| grep "$course"`; if [ `echo $ln | wc -l` -eq 1 ]; then  echo $ln >> ./missing_courses.csv; else  print $crn $course issue; fi; done

cat ./missing_courses.csv | grep -v ^$ > /tmp/missing
mv /tmp/missing ./missing_courses.csv
