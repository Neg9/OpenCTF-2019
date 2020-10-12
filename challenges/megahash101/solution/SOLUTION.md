For this challenge, you didn't even need to understand the vulnerability. If you implemented a simple collision finder, it would magically work a -lot- sooner then you would think it should.

The vulnerability is this line:

                #TODO: Investigate. Runtime error says:
                #   TypeError: Required argument 'length' (pos 1) not found
                intermediateHash = algorithm.digest(length = 2)
                
This selected a 16-bit hash length for the SHAKE step of MegaHash, limiting it to 65536 possible outputs. 

101 asks you to perform a simple collision, this is intended to be solved by simple offline brute force. This code just throws them all into a single dictionary and reports the first two that match. 

UNINTENDED SOLUTION: It turns out by default web.py is in debug mode, and you explictly have to turn that off by setting 'web.config.debug = False'. Originally the challenge didn't do that, so putting Unicode that can't be ASCII encoded into the form would cause the web server to crash and give you all local variables, including the flag. This bug was fixed around 3pm on Saturday. Thanks to team IE6 for reporting this unintended solution.

## RUN

Does not requre updates based on server.

Run solution.py. Use the two collision outputs as the webserver input. 