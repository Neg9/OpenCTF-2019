def mash(b, i):
    output = b
    output *= 3
    output ^= 0x71
    output -= i
    output += i*i*i*33
    return output & 0x7f
#end def mash(b, i)

flag_int = [ord(f) for f in 'flag{Debbie for Captain siatyVUdn6A}']

[flag_int[i] in [mash(v, i) for v in range(256)] for i in range(len(flag_int))]

print([[mash(v, i) for v in range(256)].index(flag_int[i]) for i in range(len(flag_int))])
[93, 63, 14, 10, 26, 31, 118, 65, 9, 88, 82, 35, 65, 18, 19, 27, 54, 112, 25, 15, 108, 64, 95, 11, 126, 56, 54, 63, 12, 85, 46, 103, 85, 13, 14, 60]
