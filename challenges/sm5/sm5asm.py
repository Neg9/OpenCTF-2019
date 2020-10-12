#!/usr/bin/env python3
"""
sm5asm.py It's an Assembler!
by Javantea
May 11, 2019

Based on sm5emu.

00000000  66 31 34 39 7b 52 65 76  65 72 73 69 6e 67 20 74  |f149{Reversing t|
00000010  68 65 20 4e 69 6e 74 65  6e 64 6f 20 36 34 20 43  |he Nintendo 64 C|
00000020  49 43 20 2d 20 52 45 63  6f 6e 20 32 30 31 35 7d  |IC - REcon 2015}|
00000030  0a                                                |.|
"""
from __future__ import print_function

def u8(value):
    return bytes([value])


def validateTiny(value):
    if value > 3:
        raise ValueError("Tiny value is too large {0} > 3".format(value))


def validateNibble(value):
    if value > 0xf:
        raise ValueError("Nibble value is too large 0x{0:x} > 0xf".format(value))

def validateByte(value):
    if value > 0xff:
        raise ValueError("Byte value is too large 0x{0:x} > 0xff".format(value))

# NOP
def NOP():
    return u8(0x00)

#// address control
def TR(value):
    """
    Jump to address between 0 and 0x3f.
    80 - bf
    """
    if value > 0x3f:
        raise ValueError("TR input is too large 0x{0:x} > 0x3f.".format(value))
    return u8(0x80 | value)

def TL(addr):
    """
    Jump to any address.
    """
    if addr >= (1 << 12):
        raise ValueError("Call is outside possible range (0-4095) {0:03x}".format(addr))
    return u8(0xe0 | (addr >> 8)) + u8(addr & 0xff)


def TRS(value):
    return u8(0xc0 | value)

def CALL(addr):
    """
    Use the stack to call a subroutine.
    """
    if addr >= (1 << 12):
        raise ValueError("Call is outside possible range (0-4095) {0:03x}".format(addr))
    return u8(0xf0 | (addr >> 8)) + u8(addr & 0xff)

def RTN():
    return u8(0x7D)

def RTNS():
    return u8(0x7e)

def RTN2(): #// XXX does this need any other side effects?
    return u8(0x7f)

#// data transfer
def LAX(nibble):
    """
    Load a nibble into A.
    """
    validateNibble(nibble)
    return u8(0x10 | nibble)

def LBMX(nibble):
    """
    Load a nibble into B high nibble BM.
    """
    validateNibble(nibble)
    return u8(0x30 | nibble)

def LBLX(nibble):
    """
    Load a nibble into B low nibble BL.
    """
    validateNibble(nibble)
    return u8(0x20 | nibble)

def LDA(tiny=0):
    validateTiny(tiny)
    return u8(0x50 | tiny)

def EXC(tiny=0):
    validateTiny(tiny)
    return u8(0x54 | tiny)

def EXCI(tiny=0):
    validateTiny(tiny)
    return u8(0x58 | tiny)

def EXCD(tiny=0):
    validateTiny(tiny)
    return u8(0x5c | tiny)

def EXAX():
    return u8(0x64)

def ATX():
    return u8(0x65)

def EXBM():
    return u8(0x66)

def EXBL():
    return u8(0x67)

def EX():
    return u8(0x68)


#// arithmetic
def ADX(nibble):
    validateNibble(nibble)
    return u8(0x0 | nibble)

def ADD():
    return u8(0x7a)

def ADC():
    return u8(0x7b)

def COMA():
    return u8(0x79)

def INCB():
    return u8(0x78)

def DECB():
    return u8(0x7c)

def SBX(nibble):
    """
    Artificial instruction subtract using ADX.
    """
    validateNibble(nibble)
    return u8(0x0 | (0x10 - nibble))


#// test
def TC():
    return u8(0x6e)

def TAM():
    return u8(0x6f)

def TM(tiny):
    validateTiny(tiny)
    return u8(0x48 | tiny)

def TABL():
    return u8(0x6b)

def TPB(tiny):
    validateTiny(tiny)
    return u8(0x4c | tiny)

#// bit manip
def RM(tiny):
    validateTiny(tiny)
    return u8(0x40 | tiny)

def SM(tiny):
    validateTiny(tiny)
    return u8(0x44 | tiny)

def SC():
    return u8(0x61)

def RC():
    return u8(0x60)

def ID():
    return u8(0x62)

def IE():
    return u8(0x63)

#// io control
def OUTL():
    return u8(0x71)
def OUT():
    """
    Write to port IO I believe.
    It might be mmio, but it doesn't look that way.
    """
    return u8(0x75)


#// unknown
def PAT(value):
    """
    load from ROM
    """
    validateTiny(tiny)
    validateByte(value)
    return u8(0x6a) + u8(value)

def DTA(value):
    """
    Device specific instruction (read from secret rom, analog, ...)
    """
    validateByte(value)
    return u8(0x69) + u8(value)

#// special
def HALT():
    """
    End execution.
    """
    return u8(0x77)

# ', '.join(['"{0}": {0}'.format(p) for p in x])

instructions = {"ADC": ADC, "ADD": ADD, "ADX": ADX, "ATX": ATX, "CALL": CALL, 
    "COMA": COMA, "DECB": DECB, "DTA": DTA, "EX": EX, "EXAX": EXAX, 
    "EXBL": EXBL, "EXBM": EXBM, "EXC": EXC, "EXCD": EXCD, "EXCI": EXCI, 
    "HALT": HALT, "ID": ID, "IE": IE, "INCB": INCB, "LAX": LAX, "LBLX": LBLX, 
    "LBMX": LBMX, "LDA": LDA, "NOP": NOP, "OUT": OUT, "OUTL": OUTL, 
    "PAT": PAT, "RC": RC, "RM": RM, "RTN": RTN, "RTN2": RTN2, "RTNS": RTNS, 
    "SC": SC, "SM": SM, "TABL": TABL, "TAM": TAM, "TC": TC, "TL": TL, "TM": TM, 
    "TPB": TPB, "TR": TR, "TRS": TRS, 
    # Artificial Instructions:
    "SBX": SBX}

def better_int(x):
    if x.startswith('0x'):
        return int(x[2:], 16)
    if x.startswith('0b'):
        return int(x[2:], 2)
    if x.startswith('0o'):
        return int(x[2:], 8)
    return int(x)
    

def assemble(source):
    """
    Yes, this is the assembler.
    It allows comments beginning with ; and # at the start of a line.
    Syntax:
    mnemonic
    mnemonic value
    mnemonic value value
    It does not handle labels or anything fancy like that yet.
    """
    labels = {}
    pos = 0
    machine_code = b''
    operations = 0
    lines = source.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('#'): continue
        if line.startswith(';'): continue
        # Label
        label = None
        if '#' in line:
            line = line[:line.index('#')].strip()
        if ';' in line:
            line = line[:line.index('#')].strip()
        if ':' in line:
            label, line = line.split(':', 1)
            labels[label] = pos
        #end if
        op_val = line.split()
        if len(op_val) < 1: continue
        # case insensitive
        op = op_val[0].upper()
        if op not in instructions:
            print('invalid instruction:', line)
            return None
        #end if
        instr = instructions[op]
        if len(op_val) == 1:
            machine_code += instr()
        elif len(op_val) == 2:
            if op_val[1] in labels:
                arg = labels[op_val[1]]
            else:
                arg = better_int(op_val[1])
            machine_code += instr(arg)
        elif len(op_val) == 3:
            machine_code += instr(better_int(op_val[1]), better_int(op_val[2]))
        else:
            print("Invalid line:", line)
            return None
        #end if
        pos = len(machine_code)
        operations += 1
    #next line
    print('{0} operations'.format(operations))
    return machine_code, labels
#end def assemble(source)

def test_assemble():
    source = """
LDA 3
OUT
OUT
"""
    program = assemble(sys.stdin.read())
    program2 = LDA(3) + OUT() + OUT()
    assert program == program2
    #    print("Error: Invalid program 1")
    #    exit(1)
    #end if
    

def main():
    import sys
    import argparse
    parser = argparse.ArgumentParser(description="SM5 Assembler")
    parser.add_argument('-o', '--output', nargs=1, help='Output file name, default a.out', default='a.out')
    parser.add_argument('-t', '--test', action='store_true', help='Run test only')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbosity')
    parser.add_argument('filename', nargs="?", help='SM5 input file, defaults to stdin')
    args = parser.parse_args()
    if args.test:
        return test_assemble()
    #end if
    if not args.filename:
        program = assemble(sys.stdin.read())
        if sys.hexversion >= 0x30000:
            sys.stdout.buffer.write(program)
        else:
            sys.stdout.write(program)
        #end if
        return 0
    #end if
    
    out_filename = 'a.out'
    if '-o' in sys.argv:
        pos = sys.argv.index('-o')
        out_filename = sys.argv[pos + 1]
        sys.argv.pop(pos)
        sys.argv.pop(pos)
    #end if
    filename = sys.argv[1]
    source = open(filename, 'r').read()
    program, labels = assemble(source)
    print(labels)
    open(out_filename, 'wb').write(program)
#end def main()

if __name__ == '__main__':
    main()
#end if
