#!/usr/bin/env python3

fire = open('dist/fire2','rb').read()
#print(bytes([(x ^ y) for x,y in zip(fire[:73], fire[0x82:0x82+73])]))
#fire = open('../../8086/fire2','rb').read()
for offset in range(len(fire)):
	flag = bytes([(x ^ y) for x,y in zip(fire[:73], fire[offset:offset+73])])
	if flag.startswith(b'f149{'):
		print(flag, hex(offset))
	#end if
#next offset
