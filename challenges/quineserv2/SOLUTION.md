# Quineserv2 Solution

*by Javantea*  
Mar 21, 2019 and May 4, 2019 and June 9, 2019

From the solution of quineserv, you are asked to "find the other flag". So you realize that when you cause the system to error that there is a blank flag variable. What is that about? If you put it into your solution, it prints the second flag. This ensures that they get more points if they figure out how to write a quine almost from scratch. It's actually not easy.

You start by finding an error in the program, this gives the player a hint that there is a global variable called `flag`.

```
nc challenges 9006
# ls
Traceback (most recent call last):
  File "./quineserv.py", line 41, in <module>
    exec(inp, {'__builtins__': {'print':mixprint, 'repr':repr, 'flag':''}}, {})
  File "<string>", line 1, in <module>
NameError: name 'ls' is not defined
```

In the original challenge, you had to submit a string that was a quine. Like so, this gives the flag for level 1.

Give it a quine:
```
nc challenges 9006
# y = 'y = {0};print(y.format(repr(y)))';print(y.format(repr(y)))
You win level 1. flag{If only one of us could find the time. adeb4289b6a555}
y = 'y = {0};print(y.format(repr(y)))';print(y.format(repr(y)))
```


Here you have to provide a quine, that also prints the `flag` global variable. 

Give it a quine that prints flag:
```
nc challenges 9006
# y = 'y = {0}+{1};print(y.format(repr(y),repr(flag)))'+'';print(y.format(repr(y),repr(flag)))
You win level 1. flag{If only one of us could find the time. adeb4289b6a555}
y = 'y = {0}+{1};print(y.format(repr(y),repr(flag)))'+"flag{A Sweet Sickeness, comes over me, I'm looking for something I want. lsUHNel2gLs}";print(y.format(repr(y),repr(flag)))
```
