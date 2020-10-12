#!/usr/bin/env python3
"""
HTTPS Server
by Javantea
Mar 16, 2019
Based on HTTPS Server
by Javantea
Feb 15, 2019

Threading even.

"""
import ssl
import socketserver

try:
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    from http import HTTPStatus
except ImportError:
    from BaseHTTPServer import HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    print("Boo!")
#end try

class CYOAS(HTTPServer, socketserver.ThreadingMixIn):
	"""
	Chaos.
	Secure HTTPS Server.
	"""
	def __init__(self, addr, reqhandler, *args, **kwargs):
		super().__init__(addr, reqhandler, *args, **kwargs)
		self.socket = ssl.wrap_socket(self.socket, certfile='../certkey.pem', server_side=True)
	#end def __init__(addr, reqhandler, *args, **kwargs)
#end class CYOAS(HTTPServer)

class WidevinecdmRequestHandler(SimpleHTTPRequestHandler):

    """Simple HTTP request handler with GET and HEAD commands.

    This serves files from the current directory and any of its
    subdirectories.  The MIME type for files is determined by
    calling the .guess_type() method.

    The GET and HEAD requests are identical except that the HEAD
    request omits the actual contents of the file.

    """

    server_version = "Neg9CTFHTTP/0.1"
    def __init__(self, *args, **kwargs):
        self.extensions_map['.mpd'] = 'application/dash+xml'
        super(WidevinecdmRequestHandler, self).__init__(*args, **kwargs)

    #def do_GET(self):
    #    """Serve a GET request."""
    #return super(CYOARequestHandler, self).do_GET()

    def do_POST(self):
        """ Serve a POST request."""
        if self.path == '/video.key':
            pass
        if self.path == '/no_auth':
            # FIXME: We only support content-length...
            try:
                length = self.headers.get('content-length')
            except Exception as e:
                self.send_error(
                    HTTPStatus.BAD_REQUEST,
                    "Bad content-length")
                return
            #end try
            try:
                data = self.rfile.read(int(length))
            except Exception as e:
                self.send_error(
                    HTTPStatus.BAD_REQUEST,
                    "Failed to get your data")
                return
            #end try
            v = b'{}'
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", 'application/json')
            self.send_header("Content-Length", str(len(v)))
            self.end_headers()
            self.wfile.write(v)
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
    httpd = CYOAS((args.bind, args.port), WidevinecdmRequestHandler)
    httpd.serve_forever()
#end def main()

if __name__ == '__main__':
	main()
#end if
