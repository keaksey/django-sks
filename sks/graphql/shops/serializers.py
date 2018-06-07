'''
Created on Jun 1, 2018

@author: keaksey
'''
from rest_framework import serializers
from ...shop.models import Shop
from django.contrib.sites.shortcuts import get_current_site
from ..core.serializers import SerializersMixin
from django.db import transaction, DatabaseError

class ShopSerializer(SerializersMixin, serializers.ModelSerializer):
    
    name   = serializers.CharField(max_length=256)
    domain = serializers.CharField(max_length=256, min_length=4)
    
    def validate(self, attrs):
        domain = attrs.get('domain')
        
        if Shop.objects.filter(domain__iexact=domain).exists():
            raise serializers.ValidationError({'domain': 'A shop with that name already exists.'})
        
        user = self.request.user
        
        if Shop.objects.filter(staff=user).exists():
            raise serializers.ValidationError('You already created this (%s) shop.' % domain)
        
        return attrs
    
    def create(self, validated_data):
        site = get_current_site(self.request)
        user = self.request.user
        validated_data['site'] = site
        
        try:
            
            with transaction.atomic():
                shop = super(ShopSerializer, self).create(validated_data)
                shop.add_staff(user, True)
                
        except DatabaseError as err:
            raise DatabaseError(err)
        
        return shop
    
    class Meta:
        model   = Shop
        fields  = ('name', 'domain')
