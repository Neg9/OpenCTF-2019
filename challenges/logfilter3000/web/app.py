from flask import Flask, render_template, request, Response, abort

from datetime import datetime
from uuid import uuid4
import re

import simple_orm

app = Flask(__name__)


@simple_orm.model()
class LogEntry(object):
    sev: int
    message: str
    type: str
    time: datetime



@app.route('/')
def index():
    storage = simple_orm.SQLite3Storage("db.sqlite3")
    args = {k:v for k,v in request.args.items() if v}
    results = storage.select(LogEntry, **args)
    return render_template('index.html', results = results)  
   
if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
