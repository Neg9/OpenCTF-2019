#!/usr/bin/env python3
"""
Crack Antisat
by Javantea
Originally written Sep 29, 2017

Updated: June 1, 2019

{18772, None}
Solved.
dt: 4987.308

Started: June 1, 2019 14:42
Finished: Sat 01 Jun 2019 04:05:43 PM PDT

So it took 8 threads Intel(R) Core(TM) i7-3770K CPU @ 3.50GHz
1 hour 23 minutes. But it skipped 20 rounds at the start, so... *shrug*

"""
import time
import multiprocessing

def limit_int32(x):
    # This is bad.
	y = x & 0xffffffff
	if y >= 0x80000000:
		y -= 0x100000000
	#end if
	return y
#end def limit_int32(x)

# Converted quite easily from antisat.c
def f(x, y, z, nine):
	v = limit_int32(x + y)
	w = x ^ z
	
	t = x & 0xff11ff
	u = limit_int32(y + 0xff11ff)
	a = 39297249 #limit_int32(z * nine)
	b = limit_int32(z * t) % 0x33333
	return limit_int32(v + w + t) ^ limit_int32((u & a) * b)
#end def f(x, y, z, nine)

def crackHash1(start, end=None):
	"""
	Crack a weak hash.
	"""
	# Deal with Pool
	if isinstance(start, tuple):
		start, end = start
	#end if
	for init_r in range(start, end):
		r = init_r
		for i in range(1000000):
			r = f(i, r, 393, 99993)
			#print("{0}\n".format(r))
		#next i
		if r == 178104981:
			return init_r
		#end if
	#next r
	return None
#end def crackHash1(start, end=None)


def main():
	import sys
	pool = multiprocessing.Pool()
	start = time.time()
	r = crackHash1(0, 10)
	print(r)
	print('dt: {0:3.3f}'.format(time.time()-start))
	if '-t' in sys.argv:
		return 0
	#end if
	if r != None: return 0
	start2 = time.time()
	for i in range(20,200):
		offset = i * 10 * 30
		results = pool.map(crackHash1, [(offset + 10*x, offset +10*x+10) for x in range(30)])
		results_set = set(results)
		print(results_set)
		if results_set != set([None]):
			print("Solved.")
			break
		#end if
	#next i
	print('dt: {0:3.3f}'.format(time.time()-start2))
if __name__ == '__main__':
	main()
#end if
