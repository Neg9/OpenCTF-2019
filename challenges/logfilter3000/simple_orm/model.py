import re
import datetime
from dateutil.parser import parse as dateparse

from .util import to_snake_case

_MODELS = {}

class model(object):

    def __init__(self, **kwargs):
        for attr in ["schema", "types", "fields",
                "table_name", "defaults", "type"]:
            setattr(self, "_"+attr, kwargs.get(attr))
        
        # 1. schema most athoritative 
        if self._schema:
            info = self.extract_schema_info(self._schema)
            self._table_name = info["table_name"]
            self._fields = info["fields"]
            if not self._types:
                self._types = info["types"]
        
        # 2. types are good
        if self._types and not self._fields:
            self._fields = self._types.keys()

        if not self._type:
            self._type = tuple
            

    @property
    def schema(self):
        if not self._schema:
            self._schema = self.create_schema()
        return self._schema

    @property
    def table_name(self):
        return self._table_name
    
    @property
    def fields(self):
        return self._fields

    @property
    def types(self):
        return self._types
    
    @property
    def defaults(self):
        return self._defaults if self._defaults else {}

    def create_schema(self): 
        type_map = {
            int: "INTEGER",
            str: "TEXT",
            bytes: "BLOB",
            datetime.datetime: "INTEGER", 
        }
        sql = """
        CREATE TABLE IF NOT EXISTS {table} (
            id INTEGER PRIMARY KEY,
            {columns}
        )
        """
        columns = ", ".join("{column} {type}".format(
                column=key,
                type=type_map.get(val, "TEXT")
            ) for key, val in self._types.items())
        sql = sql.format(
                table=self._table_name,
                columns=columns)

        return sql


    def extract_schema_info(self, schema):
        table_name = re.search(
            r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(?P<table_name>[A-Za-z0-9_]+)",
            schema, re.IGNORECASE).groups()[0]
        cols = re.findall(
                r"(?P<column_name>[A-Za-z0-9_]+)\s+(?P<type>[A-Za-z]+)(:?[\s\w]*(?:,\))?)*",
                re.findall(r"\([\s\w,]*\)", schema)[0], re.IGNORECASE)
        
        type_map = {
            "INTEGER": int,
            "TEXT": str,
            "BLOB": bytes,
            "REAL": float,
            "NULL": None, # ????
        }

        fields = [ k for k, _, _ in cols ]
        cols = { k: type_map.get(v.upper(), str) for k, v, _ in cols }
        return {
            "table_name": table_name,
            "fields": fields,
            "types": cols    
            }

    def __call__(self, _class):
        # sadly can't do this earlier
        if not self._table_name:
            self._table_name = to_snake_case(_class.__name__)

        if not self._types and _class.__annotations__:
            self._types = _class.__annotations__
            self._fields = self._types.keys()

        _dict =  {
            '_model' : self,
            }
       
        if self._type == tuple:
            # I may want to make this better later, maybe exec?
            def constructor(cls, *args, **kwargs):
                total_args = len(args) + len(kwargs) 
                args_dict = dict(zip(cls._model.fields, args)) 
                if total_args < len(cls._model.fields):
                    defaults = cls._model._defaults
                    defaults.update(args_dict)
                    args_dict = defaults
                args_dict.update(kwargs)
                fixed_args = list(map(args_dict.get, cls._model.fields))
                return tuple.__new__(cls, tuple(fixed_args))
            
            _dict['__slots__'] = ()
            _dict['__new__'] = constructor
            # forgive me
            _dict.update({attr: property((lambda i: (lambda self: self[i]))(i)) 
                          for i, attr in enumerate(self._fields) })
        else:
            def constructor(self, *args, **kwargs):
                total_args = len(args) + len(kwargs) 
                args_dict = dict(zip(self._model.fields, args)) 
                if total_args < len(self._model.fields):
                    defaults = self._model._defaults
                    defaults.update(args_dict)
                    args_dict = defaults
                args_dict.update(kwargs)
                fixed_args = list(map(args_dict.get, self._model.fields))
                for key, val in zip(self._model.fields, fixed_args):
                    setattr(self, key, val)
            _dict['__init__'] = constructor
        
        def factory(cls, args):
            args = list(args)
            for i, (attr, arg) in enumerate(zip(cls._model.fields, args)):
                type_ = cls._model.types[attr]
                try:
                    # have to special case datetime because I do...
                    if type_ is datetime.datetime:
                        args[i] = dateparse(arg)
                    elif type(arg) != type_:
                        args[i] = type_(arg)
                except ValueError:
                    pass

            return cls(*args)
        
        _dict['_make'] = classmethod(factory)
        
        _dict.update(_class.__dict__)

        _MODELS[_class.__name__] = self       
        return type(_class.__name__, (self._type,), _dict) 

