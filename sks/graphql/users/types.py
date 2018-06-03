'''
Created on May 21, 2018

@author: keakseysum
'''
from ...users.models import User
from ..core.types import CountableDjangoObjectType
import graphene

class User(CountableDjangoObjectType):
    is_authenticated = graphene.Boolean(
        description='List of attributes assigned to this variant.'
    )
    
    def resolve_is_authenticated(self, info):
        return info.context.user.is_authenticated
    
    class Meta:
        description = """A static page that can be manually added by a shop operator through the dashboard."""
        interfaces = [graphene.relay.Node]
        filter_fields = ['id', 'username']
        model = User