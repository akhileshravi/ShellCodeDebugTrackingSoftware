#! /bin/sh

for i in 1 2 4 5
do
cp "file$i.txt" ./subfolder
done
cd subfolder
echo file3.txt
cat file3.txt
echo ""
echo file5.txt
cat file5.txt
echo ""
echo file6.txt
cat file6.txt
cd ..
