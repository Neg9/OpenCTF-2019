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

key = os.urandom(128).hex()
iterations = int.from_bytes(os.urandom(128), byteorder='big')
key = '75ca7dbec1f460f88a71bed4c2ecce6cc9b48954d27a076215d8b776958507bce0dd85e5fa7215ee5708d2988d1eb1e720fa096348be2029958dec5956740aec0e1a1a69271352827c87e77206cd83e8c6f150a7591b38fe4f6b05896740b93f50883955e5f2eb0e38cd6d0788e5e4197c1835cd0cd82045e6aab8c9b8ac9795'
iterations = int('0xc3d7666319b735b804f7f084ee664568c7f0a85975a415ec96bede52c7d25769c77ea49f3f8e9c7c27edefcd0c32c696cd657d2245235bb503c9218c4a7a61aae339c92cca1bf5dd7fc9669ccc1ef88c668444fa192a7f9162cb38bd43f7c5df48cd5012390b3b15caae342212783a71e2e60d744e54a30c2e2a54dfa5e62ab4', 16)
masterMegaHashN = EfficientMegaHashN(iterations=iterations)
def calcHash(data):
    if not isinstance(data, bytes):
       data = data.encode('ASCII')
    tmpHash = masterMegaHashN.copy()
    tmpHash.update(data)
    return tmpHash.digest()

targetHash = bytearray.fromhex('3680c937898d5ad5819bcff031b3f2c74f39182bc9a98bbd7944fde16a86d3b88f49f6b36c54bc388bd50c7a69ba3eb99ae39d92681101e40aef8194a8623b31')
flag = open("flag.txt", "r").read()

class index:
    def GET(self):
        password = web.input().get('password')
        pow = web.input().get('pow')
        if(password is None):
            return "<html>Welcome to MegaHash 302. The password's MegaHash-" + str(iterations) + " hash is " + targetHash.hex() + '. <p><form action="\\" mode="get" onsubmit="return pow_worker()"><table><tr><th><label for="password">password</label></th><td><input id="password" name="password" type="text"> <input id="pow" name="pow" type="hidden"></td></tr><tr><th><label for="Submit"></label></th><td><button>Submit</button><p id="message"></p></td></tr></table></form><script src="/sha1.js"></script><script type="text/javascript">function pow_worker(){for(document.getElementById("message").innerHTML="Please wait, calculating proof of work. This may take a while...",password=document.getElementById("password").value,work=5,i=parseInt("AAAAAAAA",36);i<=parseInt("ZZZZZZZZ",36);i++)if(value=sha1(password+i.toString(36)),value.substr(-work)=="0".repeat(work)){document.getElementById("pow").value=i.toString(36);break}return document.getElementById("message").innerHTML="Done! Submitting...",!0}</script><p>Good luck, you\'ll need it!</html>'
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

