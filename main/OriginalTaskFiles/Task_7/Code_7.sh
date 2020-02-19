#! /bin/sh

for i in 1 2 3 4 5
do 
line='awk 'NR==$i' file9.txt'
ls $line
done
