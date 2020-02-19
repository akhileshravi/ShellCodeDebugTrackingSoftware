#! /bin/sh

line='head -1 file8.txt'
line='echo "$line Line1"'
mkdir file8_new.txt
echo "$line">file8_new.txt
cat file8_new.txt
