#pip install web.py==0.40-dev1
import web
from MegaHash import MegaHash
import os

import hmac

web.config.debug = False

urls = (
    '/', 'index'
    )

key = '4160e880ff4fbe797c8187fc37901fd9ef891fa23f12564f458965b0b73ba4a007d5f861317b84afc7bdd424d121e5650248bb27656532562b5c8fee3c9c5f4a5cc2b3d92adaa4baab6cb46d9628e4024881a0842da449f48373f4c74de9952722ffac56e67c542a746430a7aba2335be653496b8eb9417f51d24a92a07a06e1'
MegaHmac = hmac.new(key.encode('ASCII'), digestmod=MegaHash)
def GetHmac(data):
    if not isinstance(data, bytes):
       data = data.encode('ASCII')
    tmpHmac = MegaHmac.copy()
    tmpHmac.update(data)
    return tmpHmac.digest()

targetHash = GetHmac('2623c51f9170c91fd7a162e34291860effff257b43a6f7b2be760c0ec6f36917cd83fc2dc0c58ce2fc4d4c851e05e4f7e17bc46e7e390d39ef12b07610a26be8fa5d2c2da8a33b20ce2410cb253df1db448456012e6bd232c3217e1c814b043fbf78b1e2e5560753e1b3b74361a1eceb705c085e0439e4f3948e238a4d4b10ad')

flag = open("flag.txt", "r").read()

class index:
    def GET(self):
        password = web.input().get('password')
        if(password is None):
            return "<html>Welcome to MegaHash 201. The password's HMACed hash is " + targetHash.hex() + '. <p><form action="\" mode="get"><table><tr><th><label for="password">password</label></th><td><input id="password" name="password" type="text"/></td></tr><tr><th><label for="Submit"></label></th><td><button>Submit</button></td></tr></table></form><p>Good luck, you\'ll need it!</html>'
        else:
            calculatedHash = GetHmac(password.encode('ASCII'))
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

