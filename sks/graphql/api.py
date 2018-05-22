'''
Created on May 21, 2018

@author: keakseysum
'''
import graphene
import graphql_jwt
from graphene_django.filter import DjangoFilterConnectionField

from graphene_django.debug import DjangoDebug
from .core.mutations import CreateToken
from .core.filters import DistinctFilterSet

from .utils import get_node
from ..users import models as user_models

from .users.types import User
from .users.resolvers import resolve_users
from .users.mutations import UserRegister

class Query(graphene.ObjectType):
    
    user = graphene.Field(
        User, id=graphene.Argument(graphene.ID),
        description='Lookup a page by ID or by slug.')
    
    users = DjangoFilterConnectionField(
        User, filterset_class=DistinctFilterSet,
        level=graphene.Argument(graphene.Int),
        description='List of the shop\'s pages.'
    )
    
    node = graphene.Node.Field()
    debug = graphene.Field(DjangoDebug, name='__debug')
    
    def resolve_user(self, info, id=None):
        if id is not None:
            return user_models.User.objects.get(id=id)
        
        return get_node(info, id, only_type=User)
    
    def resolve_users(self, info, **kwargs):
        return resolve_users(user=info.context.user, **kwargs)
    

class Mutations(graphene.ObjectType):
    token_create = CreateToken.Field()
    token_refresh = graphql_jwt.Refresh.Field()
    
    user_register = UserRegister.Field()
    
    
schema = graphene.Schema(Query, Mutations)


