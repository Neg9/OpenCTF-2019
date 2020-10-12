# Quineserv Solution

*by Javantea*  
Mar 21, 2019 and May 4, 2019 and June 9, 2019

As the name suggests, you are required to submit a quine. Quines are readily available on the Internet, so this should be very easy.

```
nc challenges 9006
# ls
Traceback (most recent call last):
  File "./quineserv.py", line 41, in <module>
    exec(inp, {'__builtins__': {'print':mixprint, 'repr':repr, 'flag':''}}, {})
  File "<string>", line 1, in <module>
NameError: name 'ls' is not defined
```

Give it a valid python script:
```
nc challenges 9006
# a = 1
Quines win. You lose.
```

Give it a quine:
```
nc challenges 9006
# y = 'y = {0};print(y.format(repr(y)))';print(y.format(repr(y)))
You win level 1. f149{If only one of us could find the time. adeb4289b6a555}
y = 'y = {0};print(y.format(repr(y)))';print(y.format(repr(y)))
```
