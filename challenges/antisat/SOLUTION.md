# Antisat Solution
*by Javantea*  
June 1, 2019

solve.py cracks the solution using brute force (multithreaded Python). When SAT fails, use brute force. It should look like

```
python3 solve.py

dt: 15.771
{None}
...
{None}
{18772, None}
Solved.
dt: 4987.308

```

For example, with my setup:

Started: June 1, 2019 14:42  
Finished: Sat 01 Jun 2019 04:05:43 PM PDT

So on 8 threads with a Intel(R) Core(TM) i7-3770K CPU @ 3.50GHz
it took 1 hour 23 minutes. But it skipped 20 rounds at the start, so YMMV by a few hours *shrug*

If your first dt is significantly larger than 15, you will not solve it as quickly as me.
