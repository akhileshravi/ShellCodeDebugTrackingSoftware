#!/usr/bin/python
## get subprocess module
import subprocess

## call date command ##
import os
print(os.listdir())
p = subprocess.Popen("ls hello", stdout=subprocess.PIPE, shell=True)
#TODO: Take errors from the Linux Shell commands and display them

## Talk with date command i.e. read data from stdout and stderr. Store this info in tuple ##
## Interact with process: Send data to stdin. Read data from stdout and stderr, until end-of-file is reached.  ##
## Wait for process to terminate. The optional input argument should be a string to be sent to the child process, ##
## or None, if no data should be sent to the child.
(output, err) = p.communicate()
outstr = output.decode('utf-8')

def str_conv(bytes_str):
    s = ''
    for i in bytes_str:
        # bytes.
        pass

## Wait for date to terminate. Get return returncode ##
p_status = p.wait()
print("Command output : ", output)
print(type(output.decode("utf-8")))
for i in output:
    print(chr(i),end='')

# print(str(output))
print("Command exit status/return code : ", p_status)

'''
References
Run a Linux shell command and get its output (subprocess module): https://www.cyberciti.biz/faq/python-run-external-command-and-get-output/
Convert bytes to string: https://stackoverflow.com/questions/606191/convert-bytes-to-a-string
'''

print('\n Real Time Output \n')

import time

# !/usr/bin/python
import subprocess, sys

## command to run - tcp only ##
# cmd = "/bin/netstat -p tcp"
## But do not wait till netstat finish, start displaying output immediately ##

cmd = '''for i in 1 2 3 4 5;
do
    echo $i;
    sleep 1;
done'''

## run it ##
p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
t = time.time()
while time.time() - t < 10:
    out = p.stderr.read(1)
    if out == '' and p.poll() != None:
        break
    if out != '':
        sys.stdout.write(out.decode('utf-8'))
        sys.stdout.flush()

print('Completed.')