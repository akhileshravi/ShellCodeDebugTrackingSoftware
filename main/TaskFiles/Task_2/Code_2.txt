#! /bin/sh
TRIP=$(grep "New York---Tokyo" file/file.txt | wc -w)
echo Number of trip funded by host university in New York = $TRIP
COST=$(( $TRIP*1000 ))
echo Total cost funded by host university in New York = $COST$
