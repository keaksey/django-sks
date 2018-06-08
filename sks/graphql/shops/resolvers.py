'''
Created on Jun 8, 2018

@author: keakseysum
'''
from ...shop.models import Shop

def resolve_shop(info, domain, **kwargs):
    return Shop.objects.get(domain=domain)