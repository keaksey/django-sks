'''
Created on Jun 19, 2018

@author: keakseysum
'''
import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from ..core.types import CountableDjangoObjectType
from ...product import models
from .filters import ProductFilterSet

class ProductType(CountableDjangoObjectType):
    products = DjangoFilterConnectionField(
        models.Product, filterset_class=ProductFilterSet,
        description='List of products of this type.'
    )
    
    def resolve_products(self, info):
        user = info.context.user
        return models.Product.objects(user=user).filter(product_type=self).distinct()
    
    class Meta:
        description = """Represents a type of product. It defines what
        attributes are available to products of this type."""
        interfaces = [relay.Node]
        model = models.ProductType
    
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
