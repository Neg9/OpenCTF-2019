#!/usr/bin/env sage
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes

with open('public.key','rb') as f:
    pubkey = RSA.importKey(f.read())

with open('flag.enc','rb') as f:
    ct = bytes_to_long(f.read())

n = pubkey.n
e = pubkey.e

print "[*] n : {}".format(n)
print "[*] e : {}".format(e)
print "[*] ct : {}".format(ct)
print "[+] Finding roots..."

# Solve for roots of '(x^(e) - ct) mod n' where all elements are in polynomial ring GF(n)
F = GF(n)
R.<x> = F['x']
f = x^e - F(ct)
S = f.roots()

for i in xrange(len(S)):
    print "[+] Root {}: {}".format(i, S[i][0])

print "[+] Flag: {}".format(long_to_bytes(S[3][0])[203:])
