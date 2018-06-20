'''
Created on Jun 19, 2018

@author: keakseysum
'''
from .serializers import ProductSerializer

from ..core.mutations import (
    ShopSerializerMutation,
    StaffMemberRequiredMixin
)
from .types import Product as ProductType

class ProductCreateMutation(StaffMemberRequiredMixin, ShopSerializerMutation):
    permissions = 'product.edit_product'
    response_fields = ['handle']
    p1 = ProductType
    
    class Meta:
        description = 'Creates a new product.'
        serializer_class = ProductSerializer