for i in $(seq 1 100); 
do python size_estimator.py > data1/$i.dat
echo $i
done