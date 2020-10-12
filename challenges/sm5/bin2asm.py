#!/usr/bin/env python3
"""
bin2asm.py
by Javantea
May 11, 2019
"""
from sm5asm import LAX, OUT, TR, CALL, TL, ADX, SBX


flag = b'tendo 64 CIC - REcon 2015}'

program = b''
for c in flag:
    # Naive method
    program += LAX(c >> 4) + OUT() + LAX(c & 0xf) + OUT()

print(program)

program = b''
prev_a = 0xe

# TODO: Automatically generate labels from source.
labels = {'output_6': 13, 'output_65': 16, 'output_6e': 21, 'v': 26, 'push_75': 75, 'w': 80}

source = ''

for c in flag:
    # Smarter method
    if c in [0x65, 0x6e]:
        func_name = 'output_{0:02x}'.format(c)
        program += CALL(labels[func_name])
        source += 'CALL {0}\n'.format(func_name)
        prev_a = c & 0xf
        continue

    value_a = c >> 4
    value_b = c & 0xf
    cmd2 = b''
    cmd1 = b''
    if value_a != prev_a:
        dx = value_a - prev_a
        if dx > 0:
            cmd1 = ADX(dx)
            source += 'ADX {0}\nOUT\n'.format(dx)
        else:
            cmd1 = SBX(-dx) + LAX(0xe)
            source += 'SBX {0}\nLAX 0xe # SKIPPED\nOUT\n'.format(-dx)
        #end if
        prev_a = value_a
    else:
        source += 'OUT\n'
    #end if
    if value_b != prev_a:
        dx = value_b - prev_a
        if dx > 0:
            cmd2 = ADX(dx)
            source += 'ADX {0}\nOUT\n'.format(dx)
        else:
            cmd2 = SBX(-dx) + LAX(0xe)
            source += 'SBX {0}\nLAX 0xe # SKIPPED\nOUT\n'.format(-dx)
        #end if
        prev_a = value_b
    else:
        source += 'OUT\n'
    #end if
    program += cmd1 + OUT() + cmd2 + OUT()

print(source)
print(program)
