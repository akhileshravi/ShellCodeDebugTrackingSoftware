#! /bin/sh

total_icecream=2
first_student=1
second_student=1
current_student=0
for i in {3..30}
do
 	current_student=$(($first_student + $second_student ))
 	second_student=$first_student
 	first_student=$current_student
 	total_icecream=$(($total_icecream + $current_student ))	
done
print("Total number of Ice-cream = $total_icecream")