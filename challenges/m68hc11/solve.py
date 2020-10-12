"""
M68HC11 Solution
by Javantea
July 20, 2019
"""
import m68hc11_gen
import socket

data = b''

for i in m68hc11_gen.bytes_available:
	data += bytes([i])

for i in m68hc11_gen.words_available:
	data += bytes([i, 0, 0])

for i in m68hc11_gen.triples_available:
	data += bytes([i, 0, 0])

print(data)

host, port = 'challenges.openctf.cat', 9012

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(data, (host, port))
#print(s.recvfrom(1024))

#print(s.recvfrom(1024))
a = (b'', None)
while not a[0].startswith(b'# flag.S'):
	a = s.recvfrom(1024)
	print(a)

(b'# flag.S\nrolb\nclr 0x75,x\nbra 0x77\nclr 0x6f,x\nlsr 0x65,x\n.byte 0x72\nror 0x75,x\ninc 0x20,x\nasl 0x61,x\ncom 0x6b,x\npulb\nincb\npula\nror 0x11,x\ndes\ndaa\nble 0x74\nasl 0x69,x\ntxs\nbrn 0x69\ncom 0x6b20\ninc 0x7c5f\ntxs\nlsr 0x6100\nbra 0x74\npulb\ncom 0x2074\nclr 0x66,x\nbra 0x74\nasl 0x65,x\nbra 0x33\njmp 0x63,x\n.byte 0x72\nrol 0x7470\nrol 0x6f,x\njmp 0x20,x\ntst 0x65,x\nlsr 0x6f69\nlsr 0x20,x\ntsx\nror 0x20,x\ncom 0x68,x\nclr 0x49,x\ncom 0x32,x\ntst 0xffff\n', ('127.0.0.1', 6811))

open('flag.solve.S','wb').write(a[0])

print('~/src/binutils-2.32/build-m68hc11/gas/as-new -o flag.solve.bin flag.solve.S')
print('hexdump -C flag.solve.bin |less')
print('remember to use python encoding for the unprintable 7f')
