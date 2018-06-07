'''
Created on Jun 7, 2018

@author: keakseysum
'''
from ...shop.models import Shop
from ..core.types import CountableDjangoObjectType
from graphene import relay
import graphene

class Shop(CountableDjangoObjectType):
    is_owner = graphene.Boolean()
    
    def resolve_is_owner(self, info):
        return self.is_owner
    
    class Meta:
        description = """A static page that can be manually added by a shop operator through the dashboard."""
        interfaces = [relay.Node]
        filter_fields = ['id', 'domain']
        model = Shop