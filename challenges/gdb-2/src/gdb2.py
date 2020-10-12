#!/usr/bin/env python3
"""
gdb2.py
by Javantea
Jan 18-19, 2019

The very slow French Cafe method.

gdbserver localhost:4009 /bin/ls
target remote tcp::4009

b'+$qSupported:multiprocess+;swbreak+;hwbreak+;qRelocInsn+;fork-events+;vfork-events+;exec-events+;vContSupported+;QThreadEvents+;no-resumed+;xmlRegisters=i386#6a'
b'+$vMustReplyEmpty#3a'
b'+$QStartNoAckMode#b0+'
b'+$QProgramSignals:0;1;3;4;6;7;8;9;a;b;c;d;e;f;10;11;12;13;14;15;16;17;18;19;1a;1b;1c;1d;1e;1f;20;21;22;23;24;25;26;27;28;29;2a;2b;2c;2d;2e;2f;30;31;32;33;34;35;36;37;38;39;3a;3b;3c;3d;3e;3f;40;41;42;43;44;45;46;47;48;49;4a;4b;4c;4d;4e;4f;50;51;52;53;54;55;56;57;58;59;5a;5b;5c;5d;5e;5f;60;61;62;63;64;65;66;67;68;69;6a;6b;6c;6d;6e;6f;70;71;72;73;74;75;76;77;78;79;7a;7b;7c;7d;7e;7f;80;81;82;83;84;85;86;87;88;89;8a;8b;8c;8d;8e;8f;90;91;92;93;94;95;96;97;#75'

The very fast French Cafe method:

sudo tcpdump -i lo -s 0 -w /home/cap/gdb1.cap -Z nobody
scapy
a = rdpcap('gdb1.cap')
# The client:
b = [c for c in a if c.dport==4009]
# The server:
d = [c for c in a if c.sport==4009]
len([c for c in d if '\n' in str(c[TCP].payload)])
0
open('gdb_responses2.txt', 'wb').write('\n--------packet break-------\n'.join([str(c[TCP].payload) for c in d if len(c[TCP].payload)]))
open('gdb_responses2_req.txt', 'wb').write('\n--------packet break-------\n'.join([str(c[TCP].payload) for c in b if len(c[TCP].payload)]))

We send the responses based on what they send us. This is bad, but also good.

A little bit surprisingly, running this script without knowing the requests just works.
Probably because it needs to transfer a lot of data and doesn't bother to ask directions until it's ready to tell the system what to do. To the point of reading memory across before we need it *sigh*

"""
from __future__ import print_function
import socket
import threading

responses = open('gdb_communiques2.txt', 'rb').read().split(b'\n--------packet break-------\n')
requests = open('gdb_communiques2_req.txt', 'rb').read().split(b'\n--------packet break-------\n')

def checkChecksum(packet):
	"""
	gdb packets are checksummed, if we assume, then they have them.
	"""
	if len(packet) < 4:
		return False
	if packet[:1] != b'$':
		return False
	if packet[-3:-2] != b'#':
		return False
	r = hex(sum(packet[1:-3]) & 0xff)[2:].rjust(2, '0')
	#print(r)
	return (r.encode('ascii') == (packet[-2:]))
#end def checkChecksum(packet)

valid_requests = []
valid_resp = []
for req in requests:
	if req.startswith(b'+'):
		if req == b'+':
			#valid_requests.append(req)
			continue
		else:
			req = req[1:]
		#end if
	#end if
	if checkChecksum(req):
		valid_requests.append(req)
	else:
		print(req)
	#end if
#next req
for resp in responses:
	if resp.startswith(b'+'):
		if resp == b'+':
			#valid_resp.append(resp)
			continue
		else:
			resp = resp[1:]
		#end if
	#end if
	if checkChecksum(resp):
		valid_resp.append(resp)
	else:
		print(resp)
	#end if
#next resp

dupes = set()
if len(set(valid_requests)) != len(valid_requests):
	print("INFO: duplicate requests cause flaws")
	knowns = set()
	for i, packet in enumerate(valid_requests):
		if packet in knowns:
			print(packet, valid_resp[i][:20])
			dupes.add(packet)
		#end if
		knowns.add(packet)
	#next i, packet
	
#end if

print('{0}/{1} valid requests, {2}/{3} valid responses'.format(len(valid_requests), len(requests), len(valid_resp), len(responses)))

req_resp = zip(valid_requests, valid_resp)

req_resp = dict(req_resp)
#exit(1)

# The flag in a bad format, TODO: make a better format
req_resp[b'$m7fffffffd5f2,8#03'] = b'$flag{everything is everything e759d9c47a13e4974756e911cafc19f9755c37141ee6a3a76ac0df6ac358f561a0b623483cf6d1006f994d806e6957bd72a9f4c6ca9cce1d1c6530fe25c1fe05}'

# TODO: give some good hints when they request data.
# TODO: give some good hints when they step through.

def runner(ssock):
	"""
	Server thread
	"""
	needsAck = True
	partial_req = b''
	while True: #for i in range(len(responses)):
		input_data = ssock.recv(10240)
		if input_data == b'': break
		query = partial_req + input_data
		print(repr(query))
		
		req = query
		if needsAck:
			ack = query[:1]
			if ack != b'+':
				print("not acked")
			else:
				req = query[1:]
			#end if
		#end if
		# Every packet starts with $
		if b'$' != req[:1] and b'$' in req:
			req = req[req.index(b'$'):]
		#end if
		
		if req == b'$QStartNoAckMode#b0':
			needsAck = False
		#end if
		checks_out = checkChecksum(req)
		if not checks_out:
			print("bad checksum? probably partial", req)
			partial_req = query
			continue
		else:
			partial_req = b''
		#end if
		if req in req_resp:
			if req in dupes:
				print('dupe    ')
			else:
				print('known   ')#, end='')
			#end if
			resp = b'+' + req_resp[req]
		else:
			print('unknown ')#, end='')
			#resp = b"$00won't get fooled again!#29"
			# Well, it worked, so now we just need to hack the planet!
			# TODO: Step and so forth should be easy to support, right? State machine.
			resp = b'$060*"040*"40*+40*+40*+f8010*(f8010*)80*+30*"040*"38020*(38020*(38020*(1c0**1c0*+10*+10*"050*R88dd010*&88dd010**20*(10*"060*"70e3010*&70e3210*&70e3210*&58120*)8250*,20*(20*"060*"b8ed010*&b8ed210*&b8ed210*&e0010*(e0010*)80*+40*"040*"54020*(54020*(54020*(20*+20*,40**50e57464040*"4ca8010*&4ca8010*&4ca8010*&6c080*(6c080*)40**51e57464060*r10*+52e57464040*"70e3010*&70e3210*&70e3210*&900c0*(900c0*)10**#32'
		#end if
		
		# Exit
		ssock.send(resp)
	#next i
	ssock.close()
#end def runner(ssock)

def main():
	# TODO: Threaded server using async?
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Reuse the addr in case of crash.
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(('', 4009))
	s.listen(4)
	# TODO: use sockserver
	while True:
		ssock, addr = s.accept()
		print("Connected from {0}".format(addr))
		t = threading.Thread(target=runner, args=(ssock,))
		t.setDaemon(True)
		t.start()
		print("hi")
	#loop
	s.close()
#end def main()

if __name__ == '__main__':
	main()
#end if
