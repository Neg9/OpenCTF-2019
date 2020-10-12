"""
base 3
by Javantea
Dec 20, 2017

echo |sha512sum 
be688838ca8686e5c90689bf2ab585cef1137c999b48c70b92f67a5c34dc15697b5d11c982ed6d71be1e1e7f7b4e0733884aa97c3f7a339a8ed03577cf74be09  -

"""

import binascii

flag = 'flag{be_688838ca8686e5c90689bf2ab585cef1137c999b48c70b92f67a5c34dc15697b5d11c982ed6d71be1e1e7f7b4e0733884aa97c3f7a339a8ed03577cf74be09}'
flag_int = int(binascii.hexlify(flag.encode('utf-8')).decode('ascii'), 16)

# Then convert this to base 3.
# Then draw it onto a piece of paper.
# Then fax and that is your challenge.

def base3(value):
	x = value
	output = ''
	while x > 0:
		r = str(x % 3)
		output = r + output
		x //= 3
	#loop
	return output

flag_base3 = base3(flag_int)

# Encode in the creepy tick encoding
def tick_encoder(value):
	return value.replace('0', '| ').replace('1', '|| ').replace('2', '||| ')

flag_base3_tick = tick_encoder(flag_base3)

print(flag_base3_tick)
