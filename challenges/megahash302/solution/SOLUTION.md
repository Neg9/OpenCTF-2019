302 tries to make even calculating a single iteration of the hash algorithm impossible by using an absurd iteration count.

This makes building a map like we did for 301 impossible, even our cheat map would take well past the end of the universe to walk for a single input.

Instead, a small number of outputs end in a cycle after a few rounds of iteration, for instance possibly:
    [0] -> [39426] -> [6073] -> [50126] -> [39426] -> [6073]
    
Once a "path" leads into one of these cycles, the only possible output is the other values on the cycle. This means the output will naturally get "stuck" in a small number of finite cycles that can be mapped individually:
        Cycle #1 length 270 Entry point 57060.
                Cycle probability 1 in 387
                Entry probability 0.6980133056640625     entries 45745
        Cycle #2 length 99 Entry point 57995.
                Cycle probability 1 in 372
                Entry probability 0.26593017578125       entries 17428
        Cycle #3 length 5 Entry point 54972.
                Cycle probability 1 in 154
                Entry probability 0.0323944091796875     entries 2123
        Cycle #4 length 5 Entry point 59156.
                Cycle probability 1 in 2643
                Entry probability 0.00189208984375       entries 124
        Cycle #5 length 1 Entry point 20072.
                Cycle probability 1 in 1311
                Entry probability 0.000762939453125      entries 50
        Cycle #6 length 6 Entry point 22402.
                Cycle probability 1 in 8192
                Entry probability 0.000732421875         entries 48
        Cycle #7 length 3 Entry point 39426.
                Cycle probability 1 in 17873
                Entry probability 0.0001678466796875     entries 11
        Cycle #8 length 1 Entry point 4547.
                Cycle probability 1 in 65536
                Entry probability 1.52587890625e-05      entries 1
        Cycle #9 length 1 Entry point 60797.
                Cycle probability 1 in 13107
                Entry probability 7.62939453125e-05      entries 5
        Cycle #10 length 1 Entry point 17716.
                Cycle probability 1 in 65536
                Entry probability 1.52587890625e-05      entries 1
                
NOTE: This is how the "difficult" solution for MegaHash301 is derived. The entry probabity tells you how likely a random brute force search is to end up in a particular cycle, the cycle circumference then dictates how likely you are to end up on a particular output. The solution for MegaHash301 is the isolated identity point listed as "Cycle #10" in the above table. 
    
After all of these cycles are identified, you can confirm that the requested output lies on one of them. (The solution for this problem is the second point on "Cycle #7" listed above, point 6073.) Then do simple modulus math to calculate the input point on that cycle, and brute force like in 101. 

But since we're creating a fully optimized implementation of MegaHash and not just solving one challenge (for the WebServer) we do some more complex stuff:
1) While you're finding the cycles, actually calculate how "far" (in iterations) you are from the arbitrary point you define as the "entry" of the cycle. This gives you a distance and a cycle that you end on.
2) When calculating a new hash, do the first steps up to the 16-bit collision.
3) Next, consult your cycle map that tells you how far you are from a cycle, and what the cycle is (entry point & circumference).
4) Starting from your iteration count, subtract the distance to the cycle, then take the modulus of the circumference of the cycle.
5) This throws away the number of times you loop "around" the cycle, leaving only the remainder. Advance the remaining iterations of the cycle manually.
6) Calculate the remaining steps of the hash after the 16-bit collision.

Now, brute force like in 101.

UNINTENDED SOLUTION: It turns out by default web.py is in debug mode, and you explictly have to turn that off by setting 'web.config.debug = False'. Originally the challenge didn't do that, so putting Unicode that can't be ASCII encoded into the form would cause the web server to crash and give you all local variables, including the flag. This bug was fixed around 3pm on Saturday. Thanks to team IE6 for reporting this unintended solution.

## Run

To run, replace the following:
    targetHash on line 12 with the hash you are attacking
    iterations on line 10 with the iteration count
    
This solution should be substantially faster then the algorithm implemented in 301.
    
Use the "Colliding string" message as the webserver input.

## The other files in here

EfficientSelfTest.py makes sure EfficientMegaHashN works for arbitrary iteration counts (IE: doesn't have fencepost/OBO errors). 
EfficientTools.py is used to go from a numerical index to an output hash and back.
MegaHashAlgorithmsSearcher.py is what I originally used to find an algorithm ordering that had nice cycle properties for MegaHash301 & 302.
