'''
Created on Jun 19, 2018

@author: keakseysum
'''
from .serializers import ProductSerializer, VariantSerializer
from graphene import relay

from ..core.mutations import (
    ShopSerializerMutation,
    SerializerMutation,
    StaffMemberRequiredMixin
)
# 
# class VariantMutation(SerializerMutation):
#     
#     class Meta:
#         description = 'Creates a new variants.'
#         serializer_class = VariantSerializer

class ProductCreateMutation(StaffMemberRequiredMixin, ShopSerializerMutation):
    permissions = 'product.edit_product'
    
    class Meta:
        description = 'Creates a new product.'
        serializer_class = ProductSerializer
        interfaces = [relay.Node]