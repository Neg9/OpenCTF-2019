#!/usr/bin/env python3
"""
Encrypt a flag by using assembly
by Javantea
May 4, 2019

echo 'f149{this is just a test of the encryption method of choice}' > flag.bin
objdump -D -b binary -m m68hc11 flag.bin > flag.dis
m6811-elf-as -o flag.o -S flag.S
# fix it up
strings -a flag.o 
f149{this is just a yest of qhe vncryption method of yhoice}
Errors:             ^       ^   ^                    ^
spaces seem to be the main issue, so.. space t space e space c need to be avoided?
Very easy.
But programmatically because UDP.

UDP because I am that way.

mkdir tests && for i in $(seq 6 120); do python3 m68hc11_gen.py >tests/test1e"$i".txt; m6811-elf-as -o tests/test1e"$i".o test1e"$i".S; done

grep Flag tests/*.txt |less
mv -i test1e[6-9].S test1e??.S test1e???.S tests/

Found a flag that looks good enough.
"""
import sys
import collections
import struct
import random
import os.path
import opcodes.m68hc11
from socketserver import ThreadingUDPServer, DatagramRequestHandler

arch = 'cpu6811'

#Opcode = collections.namedtuple('Opcode', ['name', 'format', 'size', 'opcode', 'min_cycles', 'max_cycles', 'insn_ccr_changes', 'cpu', 'xgate_opcode_mask'])
Opcode = collections.namedtuple('Opcode', ['name', 'format', 'size', 'opcode', 'cycles_low', 'cycles_high', 'set_flags_mask', 'clear_flags_mask', 'chg_flags_mask', 'arch', 'xg_mask'])

#/* Flags when the insn only changes some CCR flags.  */
defines = {'CHG_NONE': "0,0,0",
'CHG_Z': "0,0,M6811_Z_BIT",
'CHG_C': "0,0,M6811_C_BIT",
'CHG_ZVC': "0,0,M6811_ZVC_BIT",
'CHG_NZC': "0,0,M6811_NZC_BIT",
'CHG_NZV': "0,0,M6811_NZV_BIT",
'CHG_NZVC': "0,0,M6811_NZVC_BIT",
'CHG_HNZVC': "0,0,M6811_HNZVC_BIT",
'CHG_ALL': "0,0,0xff",

#/* The insn clears and changes some flags.  */
'CLR_I': "0,M6811_I_BIT,0",
'CLR_C': "0,M6811_C_BIT,0",
'CLR_V': "0,M6811_V_BIT,0",
'CLR_V_CHG_ZC': "0,M6811_V_BIT,M6811_ZC_BIT",
'CLR_V_CHG_NZ': "0,M6811_V_BIT,M6811_NZ_BIT",
'CLR_V_CHG_ZVC': "0,M6811_V_BIT,M6811_ZVC_BIT",
'CLR_N_CHG_ZVC': "0,M6811_N_BIT,M6811_ZVC_BIT /* Used by lsr */",
'CLR_VC_CHG_NZ': "0,M6811_VC_BIT,M6811_NZ_BIT",

#/* The insn sets some flags.  */
'SET_I': "M6811_I_BIT,0,0",
'SET_C': "M6811_C_BIT,0,0",
'SET_V': "M6811_V_BIT,0,0",
'SET_Z_CLR_NVC': "M6811_Z_BIT,M6811_NVC_BIT,0",
'SET_C_CLR_V_CHG_NZ': "M6811_C_BIT,M6811_V_BIT,M6811_NZ_BIT",
'SET_Z_CHG_HNVC': "M6811_Z_BIT,0,M6811_HNVC_BIT"}

def_keys = defines.keys()

opcs = opcodes.m68hc11.m68hc11_opcodes

for opc in opcs:
    rem = None
    for i, x in enumerate(opc):
        if x in def_keys:
            a = defines[x].split(',')
            for j, v in enumerate(a):
                opc.insert(i+1+j, v)
            #next v
            rem = i
            break
    if rem != None:
        opc.pop(rem)
    #end if
    while len(opc) < 11:
        opc.append('')
    #loop
#next opc

print([opc for opc in opcs if len(opc) != 11])

opcs = list(map(lambda x: Opcode(*x), opcs))

bads = [opcode for opcode in opcs if not opcode.opcode.startswith('0x')]

assert [] == bads
bytes_available = [int(opcode.opcode.replace('0x',''),16) for opcode in opcs]

flag = 'f149{this is just a test of the encryption method of choice}'
fe = flag.encode('utf-8')
source = '# test.S\n'
for b in fe:
    if b not in bytes_available:
        source += ".db " + b
    else:
        source += opcs[bytes_available.index(b)].name + "\n"

#open('test.S','w').write(source)

opcs_none = [opc for opc in opcs if opc.format == 'OP_NONE' and arch in opc.arch]

"""
[opc.name for opc in opcs_none]
['aba', 'abx', 'asla', 'aslb', 'asld', 'asld', 'asra', 'asrb', 'bgnd', 'cba', 'clc', 'cli', 'clra', 'clrb', 'clra', 'clrb', 'clv', 'coma', 'coma', 'comb', 'comb', 'daa', 'des', 'deca', 'deca', 'decb', 'decb', 'dex', 'dey', 'ediv', 'emul', 'fdiv', 'idiv', 'inca', 'inca', 'incb', 'incb', 'ins', 'inx', 'iny', 'lsla', 'lslb', 'lsld', 'lsld', 'lsra', 'lsrb', 'lsrd', 'lsrd', 'mem', 'mul', 'mul', 'nega', 'negb', 'nop', 'nop', 'psha', 'pshb', 'pshc', 'pshd', 'pshx', 'pshx', 'pshy', 'pula', 'pulb', 'pulc', 'puld', 'pulx', 'pulx', 'puly', 'rola', 'rola', 'rolb', 'rolb', 'rora', 'rorb', 'rtc', 'rti', 'rti', 'rts', 'rts', 'sba', 'sec', 'sei', 'sev', 'stop', 'swi', 'tab', 'tap', 'tba', 'test', 'tpa', 'tsta', 'tsta', 'tstb', 'tstb', 'tsx', 'txs', 'wai', 'xgdx']


bytes_available = [int(opcode.opcode.replace('0x',''),16) for opcode in opcs_none]
source = '# test.S\n'
for b in fe:
    if b not in bytes_available:
        source += ".byte {0}\n".format(b)
    else:
        source += opcs[bytes_available.index(b)].name + "\n"

open('test0.S','w').write(source)
"""

def disassemble(fe):
    """
    Like objdump, but for hackers.
    Create m68hc11 assembly based on input.
    """
    # FIXME: Design flaw in the linker.
    address = 0
    ops_checked = set()
    source = ''
    pos = 0
    while pos < len(fe):
        b = fe[pos]
        #print(chr(b), b in words_available, b in triples_available, b in bytes_available)
        if b in words_available:
            ops_checked.add((b, 2))
            next_value = 0xff
            if (pos + 1) < len(fe): next_value = fe[pos + 1]
            opc = opcs_words[words_available.index(b)]
            if opc.format == 'OP_IX':
                source += opc.name + " 0x{0:x},x\n".format(next_value)
            elif opc.format.startswith('OP_IY'):
                source += opc.name + " 0x{0:x},x\n".format(next_value)
            elif opc.format.startswith('OP_JUMP_REL'):
                if next_value >= 0x80:
                    # Try negative?
                    next_value = next_value & 0x7f
                    source += opc.name + " -0x{0:x}\n".format(next_value)
                else:
                    source += opc.name + " 0x{0:x}\n".format(next_value)
            else:
                source += opc.name + " 0x{0:x}\n".format(next_value)
            #end if
            pos += 2
            address += 2
            continue
        if b in triples_available:
            ops_checked.add((b, 3))
            next_value = 0xffff
            if (pos + 2) < len(fe): next_value = struct.unpack('<H', bytes(fe[pos + 1:pos + 3]))[0]
            source += opcs_triples[triples_available.index(b)].name + " 0x{0:x}\n".format(next_value)
            pos += 3
            address += 3
            continue
        elif b in bytes_available:
            ops_checked.add((b, 1))
            source += opcs_none[bytes_available.index(b)].name + "\n"
        else:
            ops_checked.add(b)
            source += ".byte 0x{0:x}\n".format(b)
        pos += 1
        address += 1

    if len(ops_checked) > len(bytes_available) and len(ops_checked) == (len(set(bytes_available)) + len(set(words_available)) + len(set(triples_available))):
        raise Exception("You wonderful hacker")
    else:
        print('you got', len(ops_checked), len(bytes_available) + len(words_available) + len(triples_available))
        print(ops_checked)
    #end if
    return source
#end def disassemble(fe)

l33t_speak_encode = {'e':'3', 'l':'1', 't':'7', '{':'/', '}':'\\', 'u':'|_|', 'a':'4', 'r':'|2', 's': '5', 'o':'0'}

def mutate(data):
    """
    Input is a list, not bytes.
    Mutate data in place and return.
    If you don't want to mutate in place:
        data2 = mutate(data[:])
    If you want to mutate in place:
        mutate(data)
    If you want to add some bugs to your code:
        data3 = mutate(data)
    """
    rp = random.randint(0, len(data) - 1)
    prev = chr(data[rp])
    if prev in l33t_speak_encode:
        data[rp] = ord(l33t_speak_encode[prev][0])
        for j, jc in enumerate(l33t_speak_encode[prev][1:]):
            data.insert(rp + j + 1, ord(jc))
        #next j, jc
        print(prev, '->', l33t_speak_encode[prev])
    else:
        # Coin flip
        if random.randint(0, 1):
            # Flip least significant bit =]
            data[rp] ^= 1
            print('bit flip', bytes([data[rp] ^ 1]), '->', bytes([data[rp]]))
        else:
            # lower to upper, upper to lower, many other things to many other things.
            data[rp] ^= 0x20
            print('upper', bytes([data[rp] ^ 0x20]), '->', bytes([data[rp]]))
        #end if
    #end if
    return data
#end def mutate(data)

# Immediate, x
opcs_ix = [opc for opc in opcs if opc.format == 'OP_IX' and arch in opc.arch]
# Immediate, y
opcs_iy = [opc for opc in opcs if opc.format.startswith('OP_IY') and arch in opc.arch]
# Immediate
opcs_imm8 = [opc for opc in opcs if opc.format == 'OP_IMM8' and arch in opc.arch]
# Jump relative
opcs_jump_rel = [opc for opc in opcs if opc.format == 'OP_JUMP_REL' and arch in opc.arch]
# Index
opcs_idx = [opc for opc in opcs if opc.format == 'OP_IDX' and arch in opc.arch]

# Index 16-bit
opcs_idx16 = [opc for opc in opcs if opc.format == 'OP_IND16' and arch in opc.arch]

opcs_words = opcs_ix + opcs_iy + opcs_imm8 + opcs_jump_rel + opcs_idx
opcs_triples = opcs_idx16

bytes_available = [int(opcode.opcode.replace('0x',''),16) for opcode in opcs_none]
words_available = [int(opcode.opcode.replace('0x',''),16) for opcode in opcs_words]
triples_available = [int(opcode.opcode.replace('0x',''),16) for opcode in opcs_triples]

def gen_flag(flag, filename, iterations=200):
    """
    Data to assembly
    Input: bytes or valid unicode string
    Output: string with source code.
    """
    fe = flag
    if isinstance(flag, str):
        fe = fe.encode('utf-8')
    #end if
    min_junk = len(fe)
    best_source = ''
    fe = list(fe)
    fe_best = fe[:]

    for i in range(iterations):
        source = '# {0}\n'.format(filename) + disassemble(fe)
        lines = source.split('\n')
        byte_lines = [x for x in lines if x.startswith('.byte')]
        byte_instructions = len(byte_lines)
        if byte_instructions == 0:
            fe_best = fe
            break
        #end if
        if byte_instructions < min_junk:
            min_junk = byte_instructions
            best_source = source
            fe_best = fe
        #end if
        # TODO: Determine based on minima.
        fe = fe_best[:]
        # Random mutation
        for randmutation in range(random.randint(1, 4)):
            x = mutate(fe)
        #next randmutation
    #loop i

    print("Flag", bytes(fe_best))
    print("Bytes", byte_instructions)
    return source
#end def gen_flag(filename, iterations)

def get_flag():
    return 'f149{this is just a test of the encryption method of choice}'
#end def get_flag()

#class ThreadingUDPServer(ThreadingMixIn, UDPServer): pass

class M68HC11_Handler(DatagramRequestHandler):
    def handle(self):
        """
        Input a packet, output assembly.
        """
        # Change iterations for difficulty?
        iterations = 230
        user_input = self.request[0]
        socket = self.request[1]
        try:
            source = disassemble(user_input)
        except Exception as e:
            # How do you get it to throw an exception?
            # Deterministic to get the right flag.
            random.seed('104')
            source = gen_flag(get_flag(), 'flag.S', iterations) + '\n# ' + str(e)
        #end try
        socket.sendto(source.encode('utf-8'), self.client_address)
    #end def handle()
#end class M68HC11_Handler(DatagramRequestHandler)

def main():

    udp = False
    if '-u' in sys.argv:
        sys.argv.remove('-u')
        udp = True
    #end if

    # Deterministic.
    if len(sys.argv) > 1:
        random.seed(sys.argv[1])
    else:
        random.seed('0x31337')
    #end if
    if udp:
        port = 6811
        addr = ('0.0.0.0', port)
        server = ThreadingUDPServer(addr, M68HC11_Handler)
        server.serve_forever()
    else:
        file_iteration = 3
        while os.path.exists('test1e{0}.S'.format(file_iteration)):
            file_iteration += 1
        #loop
        filename = 'test1e{0}.S'.format(file_iteration)
        iterations = 200
        source = gen_flag(get_flag(), filename, iterations)
        open(filename,'w').write(source)
        print(filename)
    #end if
#end def main()

if __name__ == '__main__':
    main()
#end if
