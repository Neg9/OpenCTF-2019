Another difficulty ramp, 301 adds an iteration count to make neive brute force impractical in the time limits.

However, given that you have a SHAKE pigeonhole on every iteration, you can represent the entire system as a set of 16-bit pairs, from the starting point (iteration 0) to its end point (iteration 1000). 

To build this map, start with input 0 at the first SHAKE, and complete the iteration. Now continue the next iteration until you get to the same SHAKE algorithm. Record your end point, and repeat until you fill the key space. This builds a map for a single iteration of MegaHash.

Next, build a map for 100,000 iterations of MegaHash by walking your single iteration map. This allows you to calculate MegaHash-100000 as efficiently as single iteration by doing everything before SHAKE, walking the iterated map, and then doing the remainder of the steps. Calculating the final hash from a 16-bit collision can also be done ahead of time, but that's not needed for this solve.

Once you have the map, you can use your 102 solution again.

UNINTENDED SOLUTION: It turns out by default web.py is in debug mode, and you explictly have to turn that off by setting 'web.config.debug = False'. Originally the challenge didn't do that, so putting Unicode that can't be ASCII encoded into the form would cause the web server to crash and give you all local variables, including the flag. This bug was fixed around 3pm on Saturday. Thanks to team IE6 for reporting this unintended solution.

## Run

To run, replace the following:
    targetHash on line 12 with the hash you are attacking
    iterations on line 10 with the iteration count
    
NOTE: This solution takes substantial amounts of time to run on my machine. It may appear hung, here's how long the steps take on my quite old laptop:
Single transforms ~5 seconds
Iterated transforms for 100,000 ~160 seconds
Collision time ~15 seconds
    
Use the "Colliding string" message as the webserver input.