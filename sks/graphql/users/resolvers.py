'''
Created on May 21, 2018

@author: keakseysum
'''
from ...users.models import User

def resolve_users(user, **kwargs):
    if user.is_authenticated and user.is_active and user.is_staff:
        return User.objects.all().distinct()
    
    return User.objects.all().distinct()