#! /bin/sh
head -1 file10.txt
head -3 file10.txt >new_file10.txt
mv new_file10.txt file10.txt
head -1 file10.txt
