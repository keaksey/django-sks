'''
Created on May 21, 2018

@author: keakseysum
'''
from functools import wraps

from django.core.exceptions import PermissionDenied
from graphql.execution.base import ResolveInfo

def permission_denied(info):
    return PermissionDenied(
        'You have no permission to use %s' % info.field_name)
    
def permission_required(permissions):
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            info = args[1]
            assert isinstance(info, ResolveInfo)
            user = info.context.user
            input_data = kwargs.get('input')
            shop_domain = input_data.pop('shop')
            
            if not user.is_authenticated or not shop_domain:
                raise permission_denied(info)
            
            shops = user.shop_set.filter(
                staff=user,
                domain__iexact=shop_domain
            )
            
            if not shops.exists():
                raise permission_denied(info)
            
            shop = shops.get()
            setattr(info.context, 'shop', shop)
            return func(*args, **kwargs)
        return wrapper
    return decorator
