#!/usr/bin/env python3
"""
Hack the Planet!
by Javantea
Feb 14, 2019

for file in ~/src/binutils-2.30/opcodes/*-opc.c; do arch="${file%-opc.c}"; arch="$(basename "$arch")"; python3 m68hc11.py "$file" >m68hc11/"$arch".txt; done

/*
   { "test", OP_NONE,          1, 0x00,  5, _M,  CHG_NONE,  cpu6811, 0 },
                                                            +-- cpu  +-- XGATE opcode mask
  Name -+                                        +------- Insn CCR changes
  Format  ------+                            +----------- Max # cycles
  Size     --------------------+         +--------------- Min # cycles
                                   +--------------------- Opcode
*/
"""
import sys

filename = '/home/jvoss/src/binutils-2.30/opcodes/m68hc11-opc.c'
if len(sys.argv) > 1:
	filename = sys.argv[1]
#end if

arch = 'm68hc11'
if '/' in filename and '-opc' in filename:
	arch = filename[filename.rindex('/')+1:filename.index('-opc')]
#end if

a = open(filename, 'r').read().split('\n')

c = [b for b in a if b.startswith('  { "') or b.startswith('{ "') or b.startswith('  {"')]

# 1330 opcodes are you serious?

#e = [x.strip() for x in d.split(',')]

m68hc11_opcodes = []

for d in c:
	
	r = [x.strip() for x in d.split(',')]
	last = len(r) - 1
	while last > 0:
		if r[last].endswith('}'): break
		last -= 1
	#loop
	if last == 0:
		print("# Warning:", r, file=sys.stderr)
		continue
	#end if
	m68hc11_opcodes.append([r[0].replace('{ "', '').replace('"', '')] + r[1:-2] + [r[-2].replace(' }', '')])


opcodes_set = set([oc[0] for oc in m68hc11_opcodes])
len(opcodes_set)
#327

# That's a lot more reasonable.

print("{0}_opcodes = [".format(arch))
for opcode in m68hc11_opcodes:
	print(opcode, end=',\n')
#next opcode

print("]")

