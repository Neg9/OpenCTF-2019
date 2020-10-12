#pip install web.py==0.40-dev1
import web
from EfficientMegaHashN import EfficientMegaHashN
import hashlib
import os

web.config.debug = False

urls = (
    '/', 'index',
    '/sha1.js', 'sha1'
    )

iterations = 100000
masterMegaHashN = EfficientMegaHashN(iterations=iterations)
def calcHash(data):
    if not isinstance(data, bytes):
       data = data.encode('ASCII')
    tmpHash = masterMegaHashN.copy()
    tmpHash.update(data)
    return tmpHash.digest()

targetHash = bytearray.fromhex('9b0cef28257380aa5a1896e0a7192abb720ba879ad5087c6dc2b28a6f37886d4f79932069af9efd570ac60f04bc3731cb36d9e85ec03bf03c65d2b86d07c8102')
flag = open("flag.txt", "r").read()

class index:
    def GET(self):
        password = web.input().get('password')
        pow = web.input().get('pow')
        if(password is None):
            return "<html>Welcome to MegaHash 301. The password's MegaHash-" + str(iterations) + " is " + targetHash.hex() + '. <p><form action="\\" mode="get" onsubmit="return pow_worker()"><table><tr><th><label for="password">password</label></th><td><input id="password" name="password" type="text"> <input id="pow" name="pow" type="hidden"></td></tr><tr><th><label for="Submit"></label></th><td><button>Submit</button><p id="message"></p></td></tr></table></form><script src="/sha1.js"></script><script type="text/javascript">function pow_worker(){for(document.getElementById("message").innerHTML="Please wait, calculating proof of work. This may take a while...",password=document.getElementById("password").value,work=5,i=parseInt("AAAAAAAA",36);i<=parseInt("ZZZZZZZZ",36);i++)if(value=sha1(password+i.toString(36)),value.substr(-work)=="0".repeat(work)){document.getElementById("pow").value=i.toString(36);break}return document.getElementById("message").innerHTML="Done! Submitting..."+value,!0}</script><p>Good luck, you\'ll need it!</html>'
        elif(pow is None or hashlib.sha1((password + pow).encode('ASCII')).hexdigest()[-5:] != "00000"):
            return "<html>Failed proof of work.</html>";
        else:
            calculatedHash = calcHash(password)
            if(targetHash == calculatedHash):
                return "Correct! Your flag is: " + flag
            else:
                return "Incorrect hash. Calculated hash is " + calculatedHash.hex() + "."

class sha1:
    def GET(self):
        return open('sha1.js','r').read()

app = web.application(urls, globals(), True)

if __name__ == "__main__":

    #Listen on port 8000.
    import sys
    sys.argv.append('8000')

    app.run()

