perc=0.3%
if [ $# -eq 1 ]
then
  perc=$1
fi
echo $perc
java -jar spmf.jar run FPGrowth_itemsets courses.txt output.txt $perc
