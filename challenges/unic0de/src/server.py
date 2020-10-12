#!/usr/bin/env python3
"""
Unic0de Server
by Javantea
May 11, 2019
Encrypt a flag by using unic0de

Based on M68HC11
by Javantea
May 4, 2019
"""
import sys
import collections
import struct
import random
import os.path
from socketserver import ThreadingUDPServer, DatagramRequestHandler
import unic0de

data = None
passwords1 = None

def get_ton_unic0de():
    return unic0de.unic0de_r()

def get_unic0de(data):
    """
    A random selection
    """
    data_choices = []
    for i in range(random.randint(20, 40)):
        data_choices.append(data[random.randint(0, len(data) - 1)])
    return ''.join(data_choices)

def get_flag():
    return '𝐟￨' + b'\xf0\x90\x81\x9c'.decode('utf-8') + 'ɑｇ 𝗎𝕟𝜄𝖼𝐨𝕕𝑒 Տ𝒰𝑪ꓗЅ'

def smartDecode(x):
    output = None
    try:
        output = x.decode('utf-8')
    except UnicodeDecodeError as ude:
        pass
    #end try
    if output == None:
        output = x.decode('utf-16')
    #end if
    return output

class Unic0de_Handler(DatagramRequestHandler):
    def handle(self):
        """
        Input a packet, output unic0de.
        """
        # Change iterations for difficulty?
        user_input = self.request[0]
        socket = self.request[1]
        res1 = ''
        try:
            if smartDecode(user_input) in passwords1:
                res1 = get_flag()
            #end if
            res = get_unic0de(data)
        except Exception as e:
            # How do you get it to throw an exception?
            # Deterministic to get the right flag.
            random.seed('104')
            res = str(e) + get_flag()
        #end try
        res += res1
        socket.sendto(res.encode('utf-7'), self.client_address)
    #end def handle()
#end class Unic0de_Handler(DatagramRequestHandler)

def main():
    global data, passwords1
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
    data = get_ton_unic0de()
    passwords = 'A a aa aal aalii aam Aani aardvark aardwolf Aaron Aaronic Aaronical Aaronite Aaronitic Aaru Ab aba Ababdeh Ababua abac'.split(' ')
    passwords1 = []
    for password in passwords:
        # add junk to it
        p = data[random.randint(0, len(data) - 1)]
        passwords1.append(password + p)
    #next password
    if udp:
        port = 2044
        addr = ('0.0.0.0', port)
        server = ThreadingUDPServer(addr, Unic0de_Handler)
        server.serve_forever()
    else:
        res = get_unic0de(data)
        print(res.encode('utf-7'))
    #end if
#end def main()

if __name__ == '__main__':
    main()
#end if
