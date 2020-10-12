For this challenge, you didn't even need to understand the vulnerability. If you implemented a simple brute force search, it would magically work a -lot- sooner then you would think it should.

102 asks you to perform a simple 2nd preimage, this is intended to be solved by simple offline brute force for the original output. This is solvable due to the 16-bit pigeon hole. 

RealWebServer.py hardcodes the 'random' challenge key so that different docker instances don't result in different challenge hashes.

UNINTENDED SOLUTION: It turns out by default web.py is in debug mode, and you explictly have to turn that off by setting 'web.config.debug = False'. Originally the challenge didn't do that, so putting Unicode that can't be ASCII encoded into the form would cause the web server to crash and give you all local variables, including the flag. This bug was fixed around 3pm on Saturday. Thanks to team IE6 for reporting this unintended solution.

## RUN

To use the solution against a different input, replace line 13 (targetHash) with the challenge hash.

Paste the returned string as the solution into the webserver.