'''
Created on Jun 19, 2018

@author: keakseysum
'''
import graphene
from graphene import relay
# from graphene_django.filter import DjangoFilterConnectionField
from ..core.types import CountableDjangoObjectType
from ...product import models

class ProductOption(CountableDjangoObjectType):
    class Meta:
        description = """Represents an individual item for sale in the
        storefront."""
        interfaces = [relay.Node]
        model = models.Option
        
class ProductVariant(CountableDjangoObjectType):
    class Meta:
        description = """Represents an individual item for sale in the
        storefront."""
        interfaces = [relay.Node]
        model = models.ProductVariant
        
class Product(CountableDjangoObjectType):
    
    url = graphene.String(
        description='The storefront URL for the product.',
        required=True)
    
    def resolve_url(self, info):
        return self.get_absolute_url()
    
    class Meta:
        description = """Represents an individual item for sale in the
        storefront."""
        interfaces = [relay.Node]
        model = models.Product
