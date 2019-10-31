------------------------------------------------------------------------------------------------------

TASK -2

------------------------------------------------------------------------------------------------------
CONTEXT

You work in a company data record section and you have to make record text file for 10 new clients of the company with name Client_1, Client_2, ....., Cleint_10. Each file contains a line - "THIS FILE IS FOR CLIENT NUMBER - X". Here X is Client number e.g Client_1.txt contain -" THIS FILE IS FOR CLIENT NUMBER - 1". Now, the purchase departmnet need all these files. And you have to copy all the files to their folder name PURCHASE. File list all the files inside PURCHASE

Note: You are currently in the "DATA_RECORD" and the "Client_X.txt" will be made here with given text and the "PURCHASE" folder is in "DATA_RECORD" folder.
------------------------------------------------------------------------------------------------------

Pseudo Code

PROGRAM START
for i = 1 to 10 (one by one)
do 
	make a file name Client_i
	put "THIS FILE IS FOR CLEINT NUMBER - i" to file Client_i
	copy Client_i to folder PURCHASE
done 
list all the element in Purchase Folder
PRPGRAM END

------------------------------------------------------------------------------------------------------

CORRECT OUTPUT

Client_10.txt  Client_2.txt  Client_4.txt  Client_6.txt  Client_8.txt
Client_1.txt   Client_3.txt  Client_5.txt  Client_7.txt  Client_9.txt


