'''
Created on Jun 20, 2018

@author: keakseysum
'''
from rest_framework import serializers
from slugify import slugify
from rest_framework.fields import empty

from ...product.models import Product, ProductType, Category
from ..core.serializers import ShopSerializersMixin
from ..core.serializer_fields import AutoHandleField

class ProductValidateSerializerMixin(
    ShopSerializersMixin, 
    serializers.ModelSerializer
):
    
    def validate_product_type(self, value):
        handle = slugify(value).lower()
        
        product_types  = ProductType.objects.filter(
            handle__iexact=handle,
            shop=self.shop
        )
        
        product_type = None
        
        if False == product_types.exists():
            product_type = ProductType.objects.create(
                name=value, 
                handle=handle,
                shop=self.shop
            )
        else:
            product_type = product_types[0]
        
        return product_type
    
    def validate_brand(self, value):
        if not value:
            return None
        
        handle = slugify(value)
        
        categories = Category.objects.filter(
            handle__iexact=handle,
            shop=self.shop
        )
        
        category  = None
        if categories.exists() is False:
            category  = Category.objects.create(
                name=value,
                handle=handle,
                shop=self.shop
            )
        else:
            category = categories[0]
            
        return category
    
class ProductSerializer(ProductValidateSerializerMixin):
    
    def run_validation(self, attrs):
        
        if attrs == empty:
            return super().run_validation(attrs)
        
        attrs = attrs.copy()
        
        attrs['shop'] = self.shop.id
        
        return super().run_validation(attrs)
    
    product_type = serializers.CharField()
    
    category = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )
    
    handle = AutoHandleField(
        max_length=256,
        required=False,
        model_auto_handle=Product,
        uniqe_by="shop"
    )
    
    def create(self, validated_data):
        product = None
        
        try:
#             validated_data['shop'] = self.shop
            product = super(ProductSerializer, self).create(validated_data)
        except Exception as err:
            print('err ', err)
            
        return product
    
    class Meta:
        model  = Product
        fields = ('handle', 'product_type', 'category', 'shop')
        