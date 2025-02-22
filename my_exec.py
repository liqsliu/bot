#!/usr/bin/python3

import sys

#for i in sys.argv:
#  print(i)


#  await my_popen(["python3", "my_exec.py",cmd],shell=False)
# argv num = 2

if len(sys.argv) == 2:
  exec(sys.argv[1])
elif len(sys.argv) == 1:
  exec(sys.argv[0])
else:
  print("error argv num: "+ str(len(sys.argv)))


