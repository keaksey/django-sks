'''
Created on May 21, 2018

@author: keakseysum
'''
from graphene import relay, Int
from ...users.models import User
from ..core.types import CountableDjangoObjectType

class User(CountableDjangoObjectType):
    pk = Int(source="id")
    
    class Meta:
        description = """A static page that can be manually added by a shop operator through the dashboard."""
        interfaces = [relay.Node]
        filter_fields = ['id', 'username']
        model = User