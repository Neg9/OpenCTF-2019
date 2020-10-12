#pip install web.py==0.40-dev1
import web
from MegaHash import MegaHash
import os

web.config.debug = False

urls = (
    '/', 'index'
    )

#targetHash = MegaHash.hash(os.urandom(128).hex())
targetHash = MegaHash.hash('a6fdf8da8bb1cb112101351335fd722596af8f30b9763ef8d7ca58b8018a21163fe940b0d7688c7b2969fc77c88afa2d00a3d9c6acfc5524fc9f84f727791b13992b842308b9719c3543966c0cee168a57242407bba68de35522abb35f602e4d6e62527f17e3279cbc133c73dabb27e09d34ace47ccceb61fbe488b971ba7e08')

flag = open("flag.txt", "r").read()

class index:
    def GET(self):
        password = web.input().get('password')
        if(password is None):
            return "<html>Welcome to MegaHash 102. The password's hash is " + targetHash.hex() + '. <p><form action="\" mode="get"><table><tr><th><label for="password">password</label></th><td><input id="password" name="password" type="text"/></td></tr><tr><th><label for="Submit"></label></th><td><button>Submit</button></td></tr></table></form><p>Good luck, you\'ll need it!</html>'
        else:
            calculatedHash = MegaHash.hash(password.encode('ASCII'))
            if(targetHash == calculatedHash):
                return "Correct! Your flag is: " + flag
            else:
                return "Incorrect hash. Calculated hash is " + calculatedHash.hex() + "."


app = web.application(urls, globals(), True)

if __name__ == "__main__":

    #Listen on port 8000.
    import sys
    sys.argv.append('8000')

    app.run()

