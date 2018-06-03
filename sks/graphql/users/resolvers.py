'''
Created on May 21, 2018

@author: keakseysum
'''
from ...users.models import User
from ..utils import get_node
from ...users import models as user_models

def resolve_users(user, **kwargs):
    if user.is_authenticated and user.is_active and user.is_staff:
        return User.objects.all().distinct()
    
    return User.objects.all().distinct()

def resolve_user(info, **kwargs):
    pk = kwargs.get('id')
    
    if pk is not None:
        return user_models.User.objects.get(id=pk)
    
    return get_node(info, pk, only_type=User)

def resolve_user_current(user, **kwargs):
    if user.is_anonymous:
        return User(user)
    
    return user