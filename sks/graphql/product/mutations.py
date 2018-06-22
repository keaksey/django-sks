'''
Created on Jun 19, 2018

@author: keakseysum
'''
from . import serializers
from graphene import relay
import graphene

from . import types
from ..core.mutations import (
    ShopSerializerMutation,
    StaffMemberRequiredMixin
)

class ProductCreate(StaffMemberRequiredMixin, ShopSerializerMutation):
    permissions = 'product.edit_product'
    
    variants = graphene.List(
        types.ProductVariant,
        description='List of variants assigned to this product.'
    )
    
    options = graphene.List(
        types.ProductOption,
        description='List of options assigned to this product.'
    )
    
    class Meta:
        description = 'Creates a new product.'
        serializer_class = serializers.Product
        interfaces = [relay.Node]