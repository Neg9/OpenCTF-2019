#!/usr/bin/env python3
"""
AAAS Server
by Javantea
May 18, 2019

Original idea today.

Based on Unic0de Server
by Javantea
May 11, 2019

M68HC11
by Javantea
May 4, 2019
"""
import sys
import collections
import struct
import random
import os.path
from socketserver import ThreadingTCPServer, StreamRequestHandler
#import mail

data = None
passwords1 = None


def get_flag():
    return 'flag{paul graham ab3636b6f075dfea9c1d5619fb64005e0a1d5}'

class AAAS_Handler(StreamRequestHandler):
    def handle(self):
        """
        Header: Request
        Response
        """
        email = data[:]
        # Change iterations for difficulty?
        self.wfile.write(b"Email address: ")
        email_address = self.request.recv(255)
        # Clean it up a bit.
        if b'\r' in email_address: email_address = email_address.replace(b'\r', b'')
        if b'\n' in email_address: email_address = email_address.replace(b'\n', b'')
        # Refuse dictionary + letter. I don't know if this is a good idea. But at least it's realistic.
        if email_address in passwords1:
            self.wfile.write(b"Invalid email address\n")
            return
        random.seed(email_address)
        # Throw 32-bits where they will see it if they're netcatting.
        email += '{0}\n'.format(random.randint(0, 0xffffffff))
        if random.randint(0, 0xffffffff) == 987654321:
            # This is a weak solution, but we can make up for it with story.
            self.wfile.write(get_flag().encode('utf-8') + b'\n')
        #end if
        # My own templating system.
        email = email.replace('{email}', email_address.decode('utf-8', errors='replace'))
        pos = 0
        while pos < len(email):
            if 'qs=' in email[pos:]:
                next_repl = email.index('qs=', pos) + 3
                # Give them 8 bits per qs=
                rand_str = '{0:02x}'.format(random.randint(0, 0xff))
                email = email[:next_repl] + rand_str + email[next_repl + len(rand_str):]
                pos = next_repl + 5
            else:
                break
            #end if
        #loop
        self.wfile.write(email.encode('utf-8', errors='replace'))
    #end def handle()
#end class AAAS_Handler(StreamRequestHandler)

def main():
    global data, passwords1
    tcp = False
    if '-t' in sys.argv:
        sys.argv.remove('-t')
        tcp = True
    #end if

    # Deterministic.
    if len(sys.argv) > 1:
        random.seed(sys.argv[1])
    else:
        random.seed('0x31337')
    #end if
    data = open('1558121717.Vfe01I1b573a2M922672.suzy', 'rb').read().decode('utf-8', errors='replace')
    
    passwords = 'A a aa aal aalii aam Aani aardvark aardwolf Aaron Aaronic Aaronical Aaronite Aaronitic Aaru Ab aba Ababdeh Ababua abac'.split(' ')
    passwords1 = []
    for password in passwords:
        # add junk to it
        p = data[random.randint(0, len(data) - 1)]
        passwords1.append(password + p)
    #next password
    if tcp:
        port = 2045
        addr = ('0.0.0.0', port)
        server = ThreadingTCPServer(addr, AAAS_Handler)
        server.serve_forever()
    else:
        print("tcp until you think of something")
    #end if
#end def main()

if __name__ == '__main__':
    main()
#end if
