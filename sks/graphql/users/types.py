'''
Created on May 21, 2018

@author: keakseysum
'''
from ...users.models import User
from ..core.types import CountableDjangoObjectType
from ..shops.types import Shop
from ...shop import models

import graphene
from graphene import relay

class User(CountableDjangoObjectType):
    is_authenticated = graphene.Boolean(
        description='List of attributes assigned to this variant.'
    )
    
    shop = graphene.Field(
        Shop, description='get current user shop')
    
    def resolve_shop(self, info):
        user = info.context.user
        
        if not user.is_authenticated:
            return models.Shop()
        
        shop_staffs = models.ShopStaff.objects.filter(
            user=user, 
            is_owner=True
        )
        
        try:
            shop = shop_staffs.get().shop
            setattr(shop, '_is_owner', True)
        except:
            shop = models.Shop()
            
        return shop
    
    def resolve_is_authenticated(self, info):
        return info.context.user.is_authenticated
    
    class Meta:
        description = """A static page that can be manually added by a shop operator through the dashboard."""
        interfaces = [relay.Node]
        filter_fields = ['id', 'username']
        model = User