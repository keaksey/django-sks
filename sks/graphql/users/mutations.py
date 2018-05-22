'''
Created on May 22, 2018

@author: keakseysum
'''
from .serializers import RegisterSerializer

from ..core.mutations import (
    SerializerMutation
)

'''
mutation {
  userRegister(input: {
      username: "keaksey1", 
      password1: "tmppass1234", 
      email: "keaksey@gmail.com", 
      password2: "tmppass1234"
  }) {
    username
    errors {
      field
      messages
    }
  }
}
'''
class UserRegister(SerializerMutation):
    response_fields = ['username']
    
    class Meta:
        description = 'Creates a new user.'
        serializer_class = RegisterSerializer
    