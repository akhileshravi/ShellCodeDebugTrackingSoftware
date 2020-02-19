------------------------------------------------------------------------------------------------------
TASK -4
------------------------------------------------------------------------------------------------------
CONTEXT

In a class there are 30 students, on a certain day strength was 90%. On that day, the teacher took all the students to an ice-cream parlour.
Many students were eager to get ice-cream and started shouting. As a result, teacher kept a condition that 'each student will get sum of
number of ice-cream taken by it's two previous student'. Given each student bought atleast an ice-cream. Print total number of ice-cream teacher bought
that day.

Note: For first student assume that the previous two values of number of ice-cream is equal to zero.
------------------------------------------------------------------------------------------------------
Pseudo Code

PROGRAM START
total_icecream=2(first_student+second_student)
first_student=1
second_student=1
current_student=0
for i = 3 to 30 (one by one)
do 
	current_student=first_student+second_student
	second_student=first_student
	first_student=current_student
	total_icecream=total_icecream+ current_student
	
done 
print (Total number of Ice-cream= total_icecream)
PROGRAM END

------------------------------------------------------------------------------------------------------
CORRECT OUTPUT