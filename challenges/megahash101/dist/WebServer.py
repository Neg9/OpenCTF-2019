#pip install web.py==0.40-dev1
import web
from MegaHash import MegaHash

web.config.debug = False

urls = (
    '/', 'index'
    )

flag = open("flag.txt", "r").read()

class index:
    def GET(self):
        input1 = web.input().get('input1')
        input2 = web.input().get('input2')
        if(input1 is None or input2 is None):
            return '<html>Welcome to MegaHash 101. Give me two inputs that have the same output value, a cryptographic "collision".<p><form action="\" mode="get"><table><tr><th><label for="input1">Input 1</label></th><td><input name="input1" type="text"/></td></tr><tr><th><label for="input2">Input 2</label></th><td><input name="input2" type="text"/></td></tr><tr><th><label for="Submit"></label></th><td><button>Submit</button></td></tr></table></form><p>Good luck, you\'ll need it!</html>'
        else:
            calculatedHash1 = MegaHash.hash(input1.encode('ASCII'))
            calculatedHash2 = MegaHash.hash(input2.encode('ASCII'))
            if(calculatedHash1 == calculatedHash2):
                return "Correct! Your flag is: " + flag
            else:
                return "Incorrect hash. Calculated hash is " + calculatedHash1.hex() + " for Input 1 and" + calculatedHash2.hex() + " for Input 2."


app = web.application(urls, globals(), True)

if __name__ == "__main__":

    #Listen on port 8000.
    import sys
    sys.argv.append('8000')

    app.run()

