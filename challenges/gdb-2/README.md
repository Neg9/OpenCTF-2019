# GDB 2

Original Idea: 2017-09-22  
Written: 2019-01-18-2019-01-18

Score: 100

Description:
GDB server on TCP. If you use gdb it looks like a gdb server. But it is not. It's a replay of a recording of a gdb server. You have to find the flag. It's not in memory, it's in the protocol itself, which causes gdb to fail.

Category: misc

Solution: Solution.md or solve.py

Requirements:
* Python3
* gdb_communiques2.txt
* gdb_communiques2_req.txt

How to run:
python3 gdb2.py

How to exit:
Ctrl-C will exit

Challenge Text:

GDB is universal, so why doesn't it ever work? challenges:4009
