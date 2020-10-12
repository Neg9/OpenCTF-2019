#!/usr/bin/env python2
import re
"""
This will be a networked challenge that prints the contents of `banner.txt` and
accepts some commands. It should not apprear to be a python back-end at first.

Players will be able to `cat flag` for the sanity check flag.

If a specific regex is found, it would allow command pass-through
to a pwn challenge hosted in a suspiciously named directory in `/`.

TODO:
    Gracefully handle empty input
"""

def printBanner():
    with open('./banner.txt','r') as f:
        print f.read()

def printFlag():
    with open('./flag', 'r') as f:
        print f.read()

def printError(msg):
    print "bash: command not found: {}".format(msg[0])

def getInput():
    return str(raw_input('# ')).split()

def checkInputLen(msg):
    """Checks if input length is 0. If so, return to main"""
    if len(msg) == 0:
        main()

def main():
    """Disguise python to be bash - only allow `cat flag`"""

    msg = getInput()
    checkInputLen(msg)

    while msg[0] != 'exit':
        if msg[0] == "cat":
            if msg[1] == "flag":
                printFlag()
            else:
                print "cat: {}: No such file or directory".format(msg[1])
        else:
            try:
                cmd = re.findall('^\(.*\)$',''.join(msg))[0]
                print eval(cmd)
            except Exception as e:
                printError(msg)
        msg = getInput()
        checkInputLen(msg)

if __name__ == "__main__":
    printBanner()
    main()
