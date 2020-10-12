import unittest

from simple_orm import model, SQL, SELECT, INSERT


class SQLTestCase(unittest.TestCase):
    def test_models_auto_fmt(self):
        @model(fields=["id", "data"])
        class TestModel: pass

        sql = SQL("""
        SELECT {TestModel.fields}
        FROM {TestModel}
        """)
    
    def test_param_fmts(self):
        @model(fields=["id", "data"])
        class TestModel: pass

        sql = SQL("""
        SELECT {TestModel.fields}
        FROM {TestModel}
        WHERE id = {my_id}
        """, my_id=1)
