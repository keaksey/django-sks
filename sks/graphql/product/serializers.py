'''
Created on Jun 20, 2018

@author: keakseysum
'''
from rest_framework import serializers
from slugify import slugify
from rest_framework.fields import empty

from ...product import models
from ..core.serializers import ShopSerializersMixin
from ..core import SerializerField

STRING_MAX_LENGTH = 256

class ProductValidateSerializerMixin(
    ShopSerializersMixin, 
    serializers.ModelSerializer
):
    
    def validate_product_type(self, value):
        handle = slugify(value).lower()
        
        product_types  = models.ProductType.objects.filter(
            handle__iexact=handle,
            shop=self.shop
        )
        
        product_type = None
        
        if False == product_types.exists():
            product_type = models.ProductType.objects.create(
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
        
        categories = models.Category.objects.filter(
            handle__iexact=handle,
            shop=self.shop
        )
        
        category  = None
        if categories.exists() is False:
            category  = models.Category.objects.create(
                name=value,
                handle=handle,
                shop=self.shop
            )
        else:
            category = categories[0]
            
        return category

class ProductOption(serializers.ModelSerializer):
    position = serializers.IntegerField(required=False)
    
    id = serializers.IntegerField(required=False)
    
    values = serializers.SerializerMethodField('get_option_values')
    
    def run_validation(self, attrs):
        
        if attrs == empty:
            return super().run_validation(attrs)
        
        attrs = attrs.copy()
        
        if not attrs.get('position'):
            attrs['position'] = 1
            
        return super().run_validation(attrs)
    
    def get_option_values(self, option):
        product = option.product
        position = option.position
        
        if position > 3:
            position = 3
        
        option   = "option%s" % position
        
        # improve perform 
        if hasattr(product, '_prefetched_objects_cache'):
            cache_variants = product._prefetched_objects_cache.get('variants')
            
            if not cache_variants:
                return product.variants.values_list(option, flat=True)
            
            variants = []
            for cache_variant in cache_variants:
                if getattr(cache_variant, option):
                    variants.append(getattr(cache_variant, option))
                    
            return variants
        
        return product.variants.values_list(option, flat=True)
    
    class Meta:
        model  = models.Option
        fields = ('id', 'name', 'position', 'values', 'product')
        read_only_fields = ('product', 'values')

class ProductVariant(serializers.ModelSerializer):
    
    id = SerializerField.IntegerField(
        required=False,
        allow_null=True
    )
    
    price = SerializerField.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        default=0
    )
    
    compare_at_price = SerializerField.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        default=0
    )
    
    position = serializers.IntegerField(required=False)
    
#     barcode = serializers.CharField(
#         required=False,
#         allow_blank=True,
#         allow_null=True
#     )
    
    option1  = SerializerField.CharField(
        required=False,
        default='Default Title'
    )
    
    option2  = SerializerField.CharField(
        required=False,
        allow_blank=True,
        default=''
    )
    
    option3  = SerializerField.CharField(
        required=False,
        allow_blank=True,
        default=''
    )
    
    title = SerializerField.CharField(
        source='get_title',
        read_only=True
    )
    
    def run_validation(self, attrs):
        
        if attrs == empty:
            return super().run_validation(attrs)
        
        attrs = attrs.copy()
        
        if not attrs.get('compare_at_price'):
            attrs['compare_at_price'] = attrs.get('price')
            
        return super(ProductVariant, self).run_validation(attrs)
    
    class Meta:
        model = models.ProductVariant
        fields = ['id', 'option1', 'option2', 'option3', 'price', 'compare_at_price', 
            'sku', 'position', 'title'
        ]

class Product(ProductValidateSerializerMixin):
    
    id = serializers.IntegerField(
        required=False,
        read_only=True
    )
    
    title = SerializerField.CharField(
        max_length=STRING_MAX_LENGTH,
        required=True
    )
    
    product_type = SerializerField.CharField(required=True)
    
    category = SerializerField.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )
    
    handle = SerializerField.AutoHandleField(
        max_length=256,
        required=False,
        model_auto_handle=models.Product,
        uniqe_by="shop"
    )
    
    variants = ProductVariant(many=True, required=False)
    
    options = ProductOption(many=True, required=False)
    
    def run_validation(self, attrs):
        if attrs == empty:
            return super().run_validation(attrs)
        
        attrs = attrs.copy()
        attrs['shop'] = self.shop.id
        
        return super().run_validation(attrs)
    
    def create(self, validated_data):
        product = None
        print('validated_data ', validated_data)
        
        try:
            product = super(Product, self).create(validated_data)
        except Exception as err:
            print('err ', err)
            
        return product
    
    class Meta:
        model  = models.Product
        fields = ('id', 'handle', 'variants', 'options', 
            'product_type', 'category', 'shop', 'title'
        )
    
    