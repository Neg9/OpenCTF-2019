# F71 Solution

## Automation Instructions

```
apt-get install pexpect
```

Then run the solve 1000 times (To run locally, omit all 3 arguments to solve.py):

```
for i in $(seq 1 1000); do python3 solve.py <Remote Host> <Remote Port> 44 >f71_marco_monte2l"$i".txt; done
```

Once done, or while in progress use this to see if anything has returned a flag:

```
grep -h f1a9 f71_marco_monte2l* |head
```

## Solution Explanation


*by Javantea*  
Mar 21, 2019 and May 4, 2019 and June 9, 2019

I am very angry as I write this, but allow me to explain.

1. F71
Hint: All hands on deck! We've gotta get these documents to the federation before the trouble comes!
```
nc challenges.openctf.cat 9014
F71
Zone 0
0 -- 14
1 -- 9
2 -- 7
3 -- 7
4 -- 21
5 -- 17
6 -- 4
7 -- 21
8 -- 16
9 -- 16
10 -- 13
11 -- 14
12 -- 6
13 -- 10
14 -- 21 -- 1
15 -- 0 -- 12
16 -- 12 -- 4
17 -- 8 -- 14
18 -- 18 -- 8
19 -- 2 -- 4
20 -- 7 -- 14
21 -- 4 -- 4
You are at 0. You want to get to 21.
Next node:
```

They game works exactly like FTL, a _very_ popular game except no violence. It gives you a list of nodes and edges, it tells you what node you want to get to. You type the number of the node you want to visit next.

```
Next node: 14
14
x 1
You met some friendly aliens. They shared a beer with you.
You are at 14. You want to get to 21.
Next node: 21
21
x 1
You met some friendly aliens. They shared a beer with you.
Zone 1
0 -- 12
1 -- 9
2 -- 7
3 -- 2
4 -- 15
5 -- 1
6 -- 6
7 -- 8
8 -- 0
9 -- 16
10 -- 1
11 -- 12
12 -- 21
13 -- 3
14 -- 1 -- 11
15 -- 1 -- 15
16 -- 7 -- 10
17 -- 18 -- 1
18 -- 7 -- 0
19 -- 6 -- 11
20 -- 17 -- 1
21 -- 3 -- 9
You are at 0. You want to get to 21.
```

You continue this until you get to zone 7 which ends the game. You get nothing.

2. You try to automate it, so you write get_io() like is in solve.py. A while loop gets you to the end. You notice that this is a graph problem and that there are a handful of graph problems that are hard: getting to the solution as quickly as possible, getting to the solution as slowly as possible, getting to every node as quickly as possible, and getting to every possible solution.

2a. Because of the difficulty of this challenge I was encouraged to add some mention of what it takes to solve this challenge. I have added at the end discussion of alcohol being the solution to the problem.

3. This is hard so you get a network library like Small Wide World.

4. You write a function like longest_path which finds the longest path of any graph given to you by the software. Now you find that when you get above 99 visits, you get some garbage at the end of the game. 
```
'Next node: 21\r\nx 1\r\nYou met some friendly aliens. They shared a beer with you.\r\nn9YAs<mjZam\x18nwj(Kihliqf(kail\x01NMlf>9\x05\r\n\r\n\r\n'
set() [['Next node: 21'], ['x 1'], ['You met some friendly aliens. They shared a beer with you.'], ['n9YAs<mjZam\x18nwj(Kihliqf(kail\x01NMlf>9\x05'], [''], [''], ['']]
Error: missing 0 or 21 []
r []
```
That seems like a cool thing, let's go further.

5. You find that it's extremely difficult to tune this game, it's actually a fucking difficult problem to solve. FUCK! FUCK! It's fucking hard to solve this problem. It's taking hours to solve! 
6. And then you add a variable `path_length_reduction` that makes it possible for you to try over and over again automatically, and now you're done. You have solve.py and you run it thousands of times until you get the flag.

------

How does solve.py work? Well, it tries to visit as many nodes as it can, but it's not perfect. There were some bugs in earlier versions that limited the nodes it could visit, so I made the challenge easier, now it can't visit few enough nodes to win. It's original name was f71_marco_monte2.py so that is the name I am using below. You can use solve.py.

It writes files:
```
lp6.json
lp5.json
lp4.json
lp3.json
lp2.json
lp1.json
lp0.json

```

As you might expect, they are Small Wide World json files. You can throw them into https://www.small-wide-world.com/ and they will render. You'll need to sort obviously.

```
python3 f71_marco_monte2.py deb1a >f71_marco_monte2a.txt

```
Near the end of the file you see some interesting text. It doesn't fit in. What's the deal? Well, you'll find out when you get to 113 beers.
```
b'You met some friendly aliens. They shared a beer with you.\r\n'
b'q&RNdSVUu^n\x17Yx\t74vccN^}\x17\x04^R\x03faFsy!2\r\n'
```

```
for i in $(seq 1 1000); do python3 f71_marco_monte2.py deb1a 3954 44 >f71_marco_monte2l"$i".txt; done
```

1000 rounds is more than enough if you use the correct path reduction (44 was fine for me). It actually visits too many nodes. Too drunk to hack.

```
grep -h f1a9 data/f71_marco_monte2l* |head
b'f1a9{Debbie for Captain siatyVUdn6A}\r\n'
f1a9{Debbie for Captain siatyVUdn6A}
'Next node: 21\r\nx 1\r\nYou met some friendly aliens. They shared a beer with you.\r\nf1a9{Debbie for Captain siatyVUdn6A}\r\n\r\n\r\n'
set() [['Next node: 21'], ['x 1'], ['You met some friendly aliens. They shared a beer with you.'], ['f1a9{Debbie for Captain siatyVUdn6A}'], [''], [''], ['']]
b'f1a9{Debbie for Captain siatyVUdn6A}\r\n'
f1a9{Debbie for Captain siatyVUdn6A}
'Next node: 21\r\nx 1\r\nYou met some friendly aliens. They shared a beer with you.\r\nf1a9{Debbie for Captain siatyVUdn6A}\r\n\r\n\r\n'
set() [['Next node: 21'], ['x 1'], ['You met some friendly aliens. They shared a beer with you.'], ['f1a9{Debbie for Captain siatyVUdn6A}'], [''], [''], ['']]
b'f1a9{Debbie for Captain siatyVUdn6A}\r\n'
f1a9{Debbie for Captain siatyVUdn6A}

```
