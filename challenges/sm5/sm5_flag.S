

#00000000  66 31 34 39 7b 52 65 76  65 72 73 69 6e 67 20 74  |f149{Reversing t|
#00000010  68 65 20 4e 69 6e 74 65  6e 64 6f 20 36 34 20 43  |he Nintendo 64 C|
#00000020  49 43 20 2d 20 52 45 63  6f 6e 20 32 30 31 35 7d  |IC - REcon 2015}|
#00000030  0a                                                |.|

# Second flag put into memory:
# You are beautiful.
#00000000  59 6f 75 20 61 72 65 20  62 65 61 75 74 69 66 75  |You are beautifu|
#00000010  6c 2e 0a                                          |l..|

# This is what I got the first time around.
# 663439b2676727696e6707686204e696e866e8dc9ac989acfca9d6ecacbf
# This is what I got when I fixed the skip bug:
# 663134397b526576657273696e6720746865204e696e 8656e86eda7afefe9ef20eb6976585e6ec9a9c9b975e
# 22 bytes
# What I want:
# 663134397b526576657273696e6720746865204e696e 74656e646f20363420434943202d205245636f6e20323031357d
# What I got when I fixed the reverse bug:
# 663134397b526576657273696e6720746865204e696e 74656e646f20363420434943202d205245636f6e20323031357d

# Where does this happen? hahah you wish.
# The dreaded skip if BL==0xf. Fuck that's amazing.
#LAX 0x0 # SKIPPED this fixes it, so we need to not assume 0 after exci after this point..

# TODO: Use more LBMX and LBLX, that will allow you to put anything anywhere at a cost of 1 byte.
# You can also load from anywhere.
# Use PAT and DTA, TC, TAM, TM, TABL, TPB

LAX 6
OUT
OUT
#adx 0xd
sbx 3
LAX 0xe # SKIPPED
OUT
sbx 2
LAX 0xe # SKIPPED
OUT
adx 2
OUT
# 66 31 3
EXCI
# RAM: 3 0 ...
# BL = 1
adx 4
OUT
# TR v == 29
TR 29

# It's cheaper to just LAX 6 OUT hahaha
output_6:
LAX 6
OUT
RTN

output_65:
CALL output_6
# LAX would be cheaper here too.
SBX 1
LAX 0xe # SKIPPED
OUT
RTN

output_6e:
CALL output_6
ADX 8
OUT
RTN

v:
# 39
LAX 3
OUT
ADX 6
OUT

# 7b
SBX 2
LAX 0xe # SKIPPED
OUT
ADX 4
OUT

# 52
SBX 6
LAX 0xe # SKIPPED
OUT
EXCI
ADX 2
OUT

# 65
call output_65

# 76
ADX 2
OUT
SBX 1
LAX 0xe # SKIPPED
OUT

# 65 72 73 69 6e 67 20 74
call output_65
ADX 2
OUT
LAX 2
OUT
LAX 7
OUT
SBX 4
LAX 0xe # SKIPPED
OUT
ADX 3
OUT
ADX 3
OUT
EXCI
# RAM: 35 9
call output_6e
call output_6
EXCI
# RAM: 35 96
LAX 7
OUT
SBX 5
LAX 0xe # SKIPPED
OUT
LAX 0x0
OUT
ADX 0xf
EXCI
# RAM: 35 96 f
# TL w
TL 88

push_75:
LAX 7
EXCI
ADX 5
EXCI
RTN

w:
CALL push_75

LAX 7
OUT
SBX 3
LAX 0xe # SKIPPED
OUT

# So now we have 16 bytes of the flag out of 48. 1/3

# 68 65 20 4e 69 6e 74 65  6e 64 6f 20 36 34 20 43

# 68
CALL output_6
ADX 2
OUT

# Let's do a for loop for fun.

# It'd be nice to smt solve for a program that will generate this line..

call output_65
lax 2
OUT
EXCI
OUT
INCB
# RAM: 35 96 f2 0

adx 4
out
adx 0xa
out

CALL output_6
EXCI
# RAM: 35 96 f2 06
ADX 1
EXCI
# RAM: 35 96 f2 06 1
ADX 9
OUT
CALL output_6e

#> m
#   0 1 2 3 4 5 6 7 8 9 a b c d e f 
#   -------------------------------
#0: 3 5 9 6 f 7 5 2 0 6 1 0 0 0 0 0 

# next ram 72

#74 65  6e 64 6f 20 36 34 20 43  |he Nintendo 64 C|
#49 43 20 2d 20 52 45 63  6f 6e 20 32 30 31 35 7d  |IC - REcon 2015}|

# Automatically generated with bin2asm.py and then hand edited oh my gosh so much work
SBX 7
LAX 0xe # SKIPPED
OUT
EXCI
# 7 into ram, next is 2
ADX 4
OUT
CALL output_65
SBX 3
LAX 0xe # SKIPPED
EXCI
# 2 into ram, next is 65
CALL output_6e
SBX 8
LAX 0xe # SKIPPED
OUT
EXCI
# 6 into ram, next is 5
ADX 4
OUT
ADX 1
EXCI
# 5 int ram, next is 20
LAX 6
OUT
ADX 9
OUT
SBX 13
LAX 0xe # SKIPPED
OUT
EXCI 1 # 2 in ram, next is 0
LAX 0xe # The dreaded skip at 0xf!
EXCI # 0 in ram, next is 62 we're on to the next row!
OUT
ADX 3
OUT
ADX 3
OUT
EXCI # 6 in ram, next is 2
# so it gets 3 from somewhere I just don't know where from.
ADX 3
OUT
ADX 1
OUT
SBX 2
LAX 0xe # SKIPPED
OUT
EXCI # 2 is in ram, next is 65
OUT
; 0 in A, We're at CIC - REcon 2015}
ADX 4
OUT
SBX 1
LAX 0xe # SKIPPED
OUT
ADX 1
OUT

; A = 4,  we want 6, we can do it here for cheap.
ADX 2
EXCI # 6 is in ram, next is 5

ADX 9
OUT
SBX 5
LAX 0xe # SKIPPED
OUT
SBX 1
LAX 0xe # SKIPPED
OUT
# here is a fine place to do it.
ADX 2
EXCI # 5 is in ram, next is 61
ADX 2
OUT
SBX 2
LAX 0xe # SKIPPED
OUT
INCB
ADX 1
EXCD    # 1 is in place, next is 6, first use of excd ^_^;
#DECB
ADX 2
OUT
ADX 4
EXCI    # 6 is in place, increment b, next is 75
INCB
ADX 13
OUT     # d

# The stuff left to do: 75746966756c2e

# EXCI here 7
LAX 7  # first 7
EXCI
INCB
ADX 7
EXCD   # second 7

ADX 2
OUT

ADX 3
EXCI  # 5
INCB   # skip the second 7
OUT
ADX 5
OUT
SBX 3
LAX 0xe # SKIPPED
OUT
ADX 2
OUT
EXCI # 4 convenient

ADX 5
OUT
ADX 1
OUT

ATX     # X = A First use of ATX
EXCI    # 6 convenient

ADX 3
OUT     # 3
ADX 3
OUT     # 6
ADX 3
EXCI    # 9
EXAX    # X <--> A First use of EXAX
ATX     # X = A
EXCI    # 6
EXAX    # X <--> A
ATX     # X = A
EXCI    # 6
EXAX    # X <--> A
ADX 1
EXCI 3  # 7 New row!

# The dreaded 0xf skip!
LAX 0xe # SKIPPED

ADX 0xf
OUT
CALL output_6e

SBX 9
LAX 0xe # SKIPPED
EXCI    # 5

ADX 2
OUT

ADX 4
EXCI    # 6

OUT
ADX 3
OUT

adx 9
EXCI    # c

ADX 2
OUT
EXCI    # 2
ADX 3
OUT
SBX 3
LAX 0xe # SKIPPED
OUT
ADX 3
OUT
SBX 2
LAX 0xe # SKIPPED
OUT
ADX 2
OUT
ADX 2
OUT
ADX 2
OUT
ADX 6
OUT
ADX 1
EXCI    # e

# Jump to the top! That will wreck it.


# Tell them that we're done.
HALT
#HALT
