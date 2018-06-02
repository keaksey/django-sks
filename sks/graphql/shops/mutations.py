'''
Created on Jun 1, 2018

@author: keaksey
'''

from .serializers import ShopSerializer
from ..core.mutations import (
    SerializerMutation,
    LoginRequiredMixin
)

class ShopCreate(LoginRequiredMixin, SerializerMutation):
    response_fields = ['name', 'domain']
    
    class Meta:
        description = 'Creates a new shop.'
        serializer_class = ShopSerializer
    