import unittest



class TestStringMethods(unittest.TestCase):

    def test_json_encode(self):
        from Entity import Entity,Fields,EntityField,ComplexEncoder
        import json

        class MyObject(Entity):
            def __init__(self):
                self.greatfield=EntityField()

                Fields.register(self)
                super(MyObject,self).__init__()

        obj=MyObject()
        obj.greatfield=2
        dumped=json.dumps(obj,cls=ComplexEncoder)

        dict_expected=dict()
        dict_expected['id']=obj.id
        for f in Fields.fields[type(obj)]:
            dict_expected[f]=getattr(obj,f)
        expected=json.dumps(dict_expected)

        assert(expected == dumped)



