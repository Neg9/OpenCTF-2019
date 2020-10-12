import re
import sqlite3
import itertools
import datetime
import string

from collections import namedtuple

from .util import easy_decorator, to_snake_case
from .model import _MODELS

class SQLite3Storage():
    def __init__(self, filename):
        self.db = sqlite3.connect(filename)

    def create_schema(self, models):
        for model in models:
            self.db.execute(model._model.schema)


    def insert(self, model, *models, **kwargs):
        sql = INSERT(model).VALUES(model, *models)
        sql.execute(self.db)
        self.db.commit()
        return


    def select(self, model_class, **kwargs):
        cur = self.db.cursor()
        query = SELECT(model_class).WHERE(**kwargs)
        cur.execute(str(query), query.get_values())
        return list(map(model_class._make, cur.fetchall()))


class SQL_ReprWrapper(object):
    def __init__(self, model):
        self._model = model
    
    @property
    def schema(self):
        return self._model.schema

    @property
    def table_name(self):
        return self._model.table_name
    
    @property
    def fields(self):
        return ", ".join(self._model.fields)

    def __str__(self):
        return self.table_name

    def __getattr__(self, name):
        return self._model.table_name + '.' + name


class SQL(object):
    """A class to write SQL queries from models
    """
    def __init__(self, query, **kwargs):
        self._sql = query
        self._sql_formated = ''
        self.fmts = kwargs
        self._values = []
        self._models = {}
        class Value_Incrementer(object):
            INDEX = 0
            VALUES_ARRAY = self._values
            def __init__(self, value):
                self.value = value
            def __str__(self):
                self.VALUES_ARRAY.append(self.value)
                self.INDEX += 1
                return '?'
            def __repr__(self):
                return repr(self.value)
        
        self.value_incrementer = Value_Incrementer

        for key, value in kwargs.items():
            if hasattr(value, '_model'):
                self._models[key] = SQL_ReprWrapper(value._model)
            else:
                self._models[key] = Value_Incrementer(value)

    def __str__(self):
        if not self._sql_formated:
            models = { key: SQL_ReprWrapper(value) 
                    for key, value in _MODELS.items() }
            models.update(self._models) 
            self._sql_formated = self._sql.format_map(models).strip()
        return self._sql_formated

    def get_values(self):
        return self._values
    
    def execute(self, db):
        cur = db.cursor()
        cur.execute(str(self), self.get_values())
        return cur.fetchall()


class SELECT(SQL):
    def __init__(self, model):
        self._where = {}
        
        super().__init__("SELECT {Model.fields} FROM {Model} ", Model=model)

    def __getattr__(self, name):
        if name.lower() == 'where':
            def do_where(**kwargs):
                if kwargs:
                    self._where.update(kwargs)
                else:
                    self._where = {}
                return self
            return do_where
        
        raise NameError(f"{self.__class__.__name__} class has no value {name}")

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

    def get_values(self):
        return list(self._where.values())

    def __str__(self):
        sql = super().__str__()
        return sql + self.format_where()
    
    def __repr__(self):
        sql = super().__str__()
        return sql + self.format_where(safe=False)


class INSERT(SQL):
    def __init__(self, class_):
        super().__init__("INSERT INTO {Model} ({Model.fields}) VALUES ", Model=class_)
        self._insert_values = []

    def __str__(self):
        sql = super().__str__()
        value_placeholders = []
        for value in self._insert_values:
            s = "({values})".format(values=", ".join(["?"]*len(value)))
            value_placeholders.append(s)
        sql += ", ".join(value_placeholders)
        return sql

    def get_values(self):
        return list(itertools.chain(*self._insert_values))

    def __getattr__(self, name):
        if name.lower() == 'values':
            def do_values(*records):
                self._insert_values.extend(records)
                return self
            return do_values
        
        raise NameError(f"{self.__class__.__name__} class has no value {name}")

