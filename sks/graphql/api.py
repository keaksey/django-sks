'''
Created on May 21, 2018

@author: keakseysum
'''
import graphene
import logging
import graphql_jwt
from graphene_django.filter import DjangoFilterConnectionField

from graphene_django.debug import DjangoDebug
from .core.mutations import CreateToken
from .core.filters import DistinctFilterSet

from .users.types import User
from .users.resolvers import resolve_users, resolve_current_user, resolve_user
from .users.mutations import UserRegister

from .shops.mutations import ShopCreate

logger = logging.getLogger(__name__)

class Query(graphene.ObjectType):
    
    current_user = graphene.Field(
        User,
        description='get current user login'
    )
    
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
    
    def resolve_user(self, info, kwargs):
        return resolve_user(info, **kwargs)
    
    def resolve_current_user(self, info, **kwargs):
        return resolve_current_user(user=info.context.user, **kwargs)
    
    def resolve_users(self, info, **kwargs):
        return resolve_users(user=info.context.user, **kwargs)
    
class Mutations(graphene.ObjectType):
    token_create = CreateToken.Field()
    token_refresh = graphql_jwt.Refresh.Field()
    
    user_register = UserRegister.Field()
    shop_create   = ShopCreate.Field()
    
schema = graphene.Schema(Query, Mutations)


