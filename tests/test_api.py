from graphene.test import Client
from graphene import ObjectType, String, Schema
import pytest


class Query(ObjectType):
    hello = String(name=String(default_value="stranger"))

    def resolve_hello(root, info, name):
        return f'Hello {name}!'




def test_hey():
    client = Client(Schema(query=Query))
    executed = client.execute('''{hello}''')
    assert executed == {
              'data':{
                  'hello':'Hello stranger!'
                     }
              }


test_hey()    
