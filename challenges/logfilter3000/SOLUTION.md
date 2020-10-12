This is a SQL injection challenge and a python knowledge challenge

You are given the code to a web app and a library that it uses.

After looking around the code there is one place in the ORM that could be vulnerable to sql injection.

```python3
    def format_where(self, safe=True):
        where_fmts = []
        for key, val in self._where.items():
            if safe: 
                where_fmts.append("{} = ?".format(key))
            else:
                where_fmts.append("{} = {}".format(key, repr(val)))
        if where_fmts:
            return " WHERE " + " AND ".join(where_fmts)
        return ""
```

After you find this you should be able to start with some SQL injection.
The injection point is in the *key* of the query parameters. 

You know that the db is sqlite3 so you can dump the schema from `sqlite_master`
and see that `log_entry` has a hidden column. There is one row that has a value 
in that column and it has the id 1337.


