'''
Created on Jun 19, 2018

@author: keakseysum
'''
import graphene
from graphene.types import InputObjectType

from ..core.mutations import (
    SerializerMutation,
    StaffMemberRequiredMixin
)

class ProductTypeCreateMutation(StaffMemberRequiredMixin, SerializerMutation):
    permissions = 'product.edit_properties'
    
    class Meta:
        description = 'Creates a new product type.'
        
class CategoryCreateMutation(StaffMemberRequiredMixin, SerializerMutation):
    permissions = 'category.edit_category'
    
    class Meta:
        description = 'Creates a new category.'
        #form_class = CategoryForm

class ProductCreateMutation(StaffMemberRequiredMixin, SerializerMutation):
    permissions = 'product.edit_product'
    
    class Meta:
        description = 'Creates a new product.'
        #form_class = ProductForm
        # Exclude from input form fields
        # that are being overwritten by arguments
        exclude = ['product_type', 'category', 'attributes']
        