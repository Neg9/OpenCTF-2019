201 requires you to solve an HMAC with an unknown key. Difficulty ramps up here, you actually have to understand the flaw before you can attack this problem (unless you use one of the unintended solutions at the end of this section.)

See https://en.wikipedia.org/wiki/HMAC for HMAC definition. When K is larger then the HMAC block size, it is hashed down to the block size. This means K's full influence on the output is _after_ going through MegaHash. That means it's subject to brute force.

Write your own HMAC implementation that takes as input the key _hash_ instead of the key. Enumerate all known key hashes (65535 of them). 
    Implementation detail of solution.py: To make it fast, we can start from the last SHAKE algorithm and replace it with all numbers 0...65535 (deterministic brute force). This saves the work of brute forcing the early steps of the algorithm and a probabilistic brute force.

Ask for the hash for a known output. Find all possible key hashes that could produce that output.

Ask for a second hash, figure out which key hashes validate for both pairs. This gives you a unique key hash, from which you do a brute force like 101.

UNINTENDED SOLUTION #1: Yeah, you can brute force the server because the key space is so small and I neglected to add a proof of work. Props to team Psychoholics for solving it first and without doing a brute force on the server. After this, I quickly added a PoW to 301 and 302 before they opened the next morning. 

UNINTENDED SOLUTION #2: It turns out by default web.py is in debug mode, and you explictly have to turn that off by setting 'web.config.debug = False'. Originally the challenge didn't do that, so putting Unicode that can't be ASCII encoded into the form would cause the web server to crash and give you all local variables, including the flag. This bug was fixed around 3pm on Saturday. Thanks to team IE6 for reporting this unintended solution.

## Run

To run, replace the following:
    targetHash on line 21 with the hash you are attacking
    Replace knownValues on line 25-26 with known input/ouput pairs
    
Use the "Another password that collides using HMAC key" as the webserver input.