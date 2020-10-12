#!/usr/bin/env python3
"""
HTTPS Server
by Javantea
Feb 15, 2019

Threading even.

Options on a normal connection:
[('ECDHE-RSA-AES256-GCM-SHA384', 'TLSv1/SSLv3', 256),
('ECDHE-ECDSA-AES256-GCM-SHA384', 'TLSv1/SSLv3', 256),
('ECDH-RSA-AES256-GCM-SHA384', 'TLSv1/SSLv3', 256),
('ECDH-ECDSA-AES256-GCM-SHA384', 'TLSv1/SSLv3', 256),
('ECDHE-RSA-AES128-GCM-SHA256', 'TLSv1/SSLv3', 128),
('ECDHE-ECDSA-AES128-GCM-SHA256', 'TLSv1/SSLv3', 128),
('ECDH-RSA-AES128-GCM-SHA256', 'TLSv1/SSLv3', 128),
('ECDH-ECDSA-AES128-GCM-SHA256', 'TLSv1/SSLv3', 128),
('DH-DSS-AES256-GCM-SHA384', 'TLSv1/SSLv3', 256),
('DHE-DSS-AES256-GCM-SHA384', 'TLSv1/SSLv3', 256),
('DH-RSA-AES256-GCM-SHA384', 'TLSv1/SSLv3', 256),
('DHE-RSA-AES256-GCM-SHA384', 'TLSv1/SSLv3', 256),
('DH-DSS-AES128-GCM-SHA256', 'TLSv1/SSLv3', 128),
('DHE-DSS-AES128-GCM-SHA256', 'TLSv1/SSLv3', 128),
('DH-RSA-AES128-GCM-SHA256', 'TLSv1/SSLv3', 128),
('DHE-RSA-AES128-GCM-SHA256', 'TLSv1/SSLv3', 128),
('ECDHE-RSA-AES256-SHA384', 'TLSv1/SSLv3', 256),
('ECDHE-ECDSA-AES256-SHA384', 'TLSv1/SSLv3', 256),
('ECDHE-RSA-AES256-SHA', 'TLSv1/SSLv3', 256),
('ECDHE-ECDSA-AES256-SHA', 'TLSv1/SSLv3', 256),
('ECDH-RSA-AES256-SHA384', 'TLSv1/SSLv3', 256),
('ECDH-ECDSA-AES256-SHA384', 'TLSv1/SSLv3', 256),
('ECDH-RSA-AES256-SHA', 'TLSv1/SSLv3', 256),
('ECDH-ECDSA-AES256-SHA', 'TLSv1/SSLv3', 256),
('DHE-RSA-AES256-SHA256', 'TLSv1/SSLv3', 256),
('DHE-DSS-AES256-SHA256', 'TLSv1/SSLv3', 256),
('DH-RSA-AES256-SHA256', 'TLSv1/SSLv3', 256),
('DH-DSS-AES256-SHA256', 'TLSv1/SSLv3', 256),
('DHE-RSA-AES256-SHA', 'TLSv1/SSLv3', 256),
('DHE-DSS-AES256-SHA', 'TLSv1/SSLv3', 256),
('DH-RSA-AES256-SHA', 'TLSv1/SSLv3', 256),
('DH-DSS-AES256-SHA', 'TLSv1/SSLv3', 256),
('ECDHE-RSA-AES128-SHA256', 'TLSv1/SSLv3', 128),
('ECDHE-ECDSA-AES128-SHA256', 'TLSv1/SSLv3', 128),
('ECDHE-RSA-AES128-SHA', 'TLSv1/SSLv3', 128),
('ECDHE-ECDSA-AES128-SHA', 'TLSv1/SSLv3', 128),
('ECDH-RSA-AES128-SHA256', 'TLSv1/SSLv3', 128),
('ECDH-ECDSA-AES128-SHA256', 'TLSv1/SSLv3', 128),
('ECDH-RSA-AES128-SHA', 'TLSv1/SSLv3', 128),
('ECDH-ECDSA-AES128-SHA', 'TLSv1/SSLv3', 128),
('DHE-RSA-AES128-SHA256', 'TLSv1/SSLv3', 128),
('DHE-DSS-AES128-SHA256', 'TLSv1/SSLv3', 128),
('DH-RSA-AES128-SHA256', 'TLSv1/SSLv3', 128),
('DH-DSS-AES128-SHA256', 'TLSv1/SSLv3', 128),
('DHE-RSA-AES128-SHA', 'TLSv1/SSLv3', 128),
('DHE-DSS-AES128-SHA', 'TLSv1/SSLv3', 128),
('DH-RSA-AES128-SHA', 'TLSv1/SSLv3', 128),
('DH-DSS-AES128-SHA', 'TLSv1/SSLv3', 128),
('DHE-RSA-CAMELLIA256-SHA', 'TLSv1/SSLv3', 256),
('DHE-DSS-CAMELLIA256-SHA', 'TLSv1/SSLv3', 256),
('DH-RSA-CAMELLIA256-SHA', 'TLSv1/SSLv3', 256),
('DH-DSS-CAMELLIA256-SHA', 'TLSv1/SSLv3', 256),
('DHE-RSA-CAMELLIA128-SHA', 'TLSv1/SSLv3', 128),
('DHE-DSS-CAMELLIA128-SHA', 'TLSv1/SSLv3', 128),
('DH-RSA-CAMELLIA128-SHA', 'TLSv1/SSLv3', 128),
('DH-DSS-CAMELLIA128-SHA', 'TLSv1/SSLv3', 128),
('AES256-GCM-SHA384', 'TLSv1/SSLv3', 256),
('AES128-GCM-SHA256', 'TLSv1/SSLv3', 128),
('AES256-SHA256', 'TLSv1/SSLv3', 256),
('AES256-SHA', 'TLSv1/SSLv3', 256),
('AES128-SHA256', 'TLSv1/SSLv3', 128),
('AES128-SHA', 'TLSv1/SSLv3', 128),
('CAMELLIA256-SHA', 'TLSv1/SSLv3', 256),
('CAMELLIA128-SHA', 'TLSv1/SSLv3', 128)]

Options on a weird connection:
???

"""
import ssl
import socketserver

try:
	from http.server import HTTPServer, SimpleHTTPRequestHandler
except ImportError:
	from BaseHTTPServer import HTTPServer
	from SimpleHTTPServer import SimpleHTTPRequestHandler
	print("Boo!")
#end try

class CYOAS(HTTPServer, socketserver.ThreadingMixIn):
	"""
	Chaos.
	Choose your own adventure Secure HTTPS Server.
	"""
	def __init__(self, addr, reqhandler, *args, **kwargs):
		super().__init__(addr, reqhandler, *args, **kwargs)
		self.socket = ssl.wrap_socket(self.socket, certfile='../certkey.pem', server_side=True)
	#end def __init__(addr, reqhandler, *args, **kwargs)
#end class CYOAS(HTTPServer)

class CYOARequestHandler(SimpleHTTPRequestHandler):

    """Simple HTTP request handler with GET and HEAD commands.

    This serves files from the current directory and any of its
    subdirectories.  The MIME type for files is determined by
    calling the .guess_type() method.

    The GET and HEAD requests are identical except that the HEAD
    request omits the actual contents of the file.

    """

    server_version = "Neg9CTFHTTP/0.1"

    def do_GET(self):
        """Serve a GET request."""
        cipher = self.request.cipher()
        if len(cipher) == 3 and cipher == ('CAMELLIA128-SHA', 'TLSv1/SSLv3', 128):
            f = self.send_head()
            self.wfile.write(b"flag{Sporochnaceae-granulate_microlith+tillering}\n")
        else:
            f = self.send_head()
            if f:
                try:
                    self.copyfile(f, self.wfile)
                finally:
                    f.close()
#end class CYOARequestHandler(SimpleHTTPRequestHandler)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--bind', '-b', default='', metavar='ADDRESS',
                        help='Specify alternate bind address '
                             '[default: all interfaces]')
    parser.add_argument('port', action='store',
                        default=4443, type=int,
                        nargs='?',
                        help='Specify alternate port [default: 4443]')
    args = parser.parse_args()
    httpd = CYOAS((args.bind, args.port), CYOARequestHandler)
    httpd.serve_forever()
#end def main()

if __name__ == '__main__':
	main()
#end if
