#! /bin/sh

total_distance=0
step_distance=10
for i in {1..4}
do 
total_distance=$(($total_distance+$step_distance))
done
echo "Distance between Mr. X Home and Workplace= $total_distance"