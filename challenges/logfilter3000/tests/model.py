import unittest

from simple_orm import model, SQLite3Storage


class ModelTestCase(unittest.TestCase):
    def test_api(self):
        @model(schema="""
        CREATE TABLE Testing_Table (
            id INTEGER PRIMARY KEY,
            data BLOB
        )""")
        class TestModel: pass
        
        @model(fields=["id", "data"])
        class TestModel: pass

        @model(types={"id": int, "data": bytes})
        class TestModel: pass


    def test_simple_define_model(self):
       
        @model(types={"one":int, "two":int, "three":int})
        class TestModel: pass

        storage = SQLite3Storage(":memory:")
        test_model = TestModel(1,2,3)
        storage.create_schema([TestModel])
        
        storage.insert(test_model)
        results = storage.select(TestModel)
        self.assertIn(test_model, results)

        self.assertEqual(test_model.one, 1)
        self.assertEqual(test_model.two, 2)
        self.assertEqual(test_model.three, 3)


    def test_manual_table_def(self):
        @model(schema="""
        CREATE TABLE Testing_Table (
            id INTEGER PRIMARY KEY,
            data BLOB
        )""")
        class TestModel: pass

        self.assertEqual(TestModel._model.table_name, "Testing_Table")
        self.assertTrue(hasattr(TestModel, "id"))
        self.assertTrue(hasattr(TestModel, "data"))
        self.assertTrue(isinstance(TestModel(data=0, id=22), tuple)) 


    def test_defaults(self):
        @model(fields=["a", "b"],
                defaults={"a": 1, "b": 2})
        class TestModel: pass
        m = TestModel()
        self.assertEqual(m.a, 1)
        self.assertEqual(m.b, 2)
        
        m = TestModel(3)
        self.assertEqual(m.a, 3)
        self.assertEqual(m.b, 2)
        
        m = TestModel(a=3)
        self.assertEqual(m.a, 3)
        self.assertEqual(m.b, 2)


    def test_type_convertion(self):
        @model(types={"one":int, "two":int, "three":int})
        class TestModel: pass
    
        m = TestModel._make(("1", "2", "3"))
        self.assertEqual(type(m.one), int)
    
    
    def test_type_param(self):
        @model(type=object,
            types={"one":int, "two":int, "three":int})
        class TestModel: pass
    
        m = TestModel("1", "2", "3")
        m.one = 2
        
        @model(type=tuple,
            types={"one":int, "two":int, "three":int})
        class TestModel: pass
   
        try:
            m = TestModel("1", "2", "3")
            m.one = 2
        except:
            pass
        else:
            raise Exception("Tuple class is mutable")

    def test_sqli(self):
        @model(types={"one":int, "two":int, "three":int})
        class TestModel: pass
        
        storage = SQLite3Storage(":memory:")
        storage.create_schema([TestModel])
        item = TestModel(1,2,3)
        storage.insert(item)
        self.assertIn(item, storage.select(TestModel, **{"1=1 or '2'":"2"}))
