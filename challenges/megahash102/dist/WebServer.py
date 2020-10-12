#pip install web.py==0.40-dev1
import web
from MegaHash import MegaHash
import os

urls = (
    '/', 'index'
    )

targetHash = MegaHash.hash(os.urandom(128).hex())

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

