'''
Created on Jun 1, 2018

@author: keaksey
'''
from rest_framework import serializers
from ...shop.models import Shop

class ShopSerializer(serializers.ModelSerializer):
    
    name = serializers.CharField(max_length=256, min_length=8)
    
    class Meta:
        model = Shop
        fields = ('name', )
