'''
Created on Jun 7, 2018

@author: keakseysum
'''
from ...shop.models import Shop
from ..core.types import CountableDjangoObjectType
from graphene import relay
import graphene

class Theme(graphene.ObjectType):
    name = graphene.String()
    src  = graphene.String()
    
    def resolve_name(self, info):
        return 'SreyKeo'
    
    def resolve_src(self, info):
        return '/SreyKeo'
    
class Shop(CountableDjangoObjectType):
    is_owner = graphene.Boolean()
    
    current_theme = graphene.Field(
        Theme, description='get current shop theme'
    )
    
    def resolve_current_theme(self, info):
        return Theme()
    
    def resolve_is_owner(self, info):
        return self.is_owner
    
    
    class Meta:
        description = """A static page that can be manually added by a shop operator through the dashboard."""
        interfaces = [relay.Node]
        filter_fields = ['id', 'domain']
        model = Shop