#! /bin/sh

a=131267
b=131050
c=134200
d=131311
ac=$(($a*$c))
bd=$(($b*$d))
if [ $ac -gt $bd ]
then
echo ac is greater than bd
fi
if [ $bd -gt $ac ]
then
echo ac is not greater than bd
fi