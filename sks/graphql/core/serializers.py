'''
Created on Jun 7, 2018

@author: keakseysum
'''
class SerializersMixin(object):
    
    def __init__(self, *args, **kwargs):
        super(SerializersMixin, self).__init__(*args, **kwargs)
        self.request = self.context.get('request')
        self.user    = None
        
        if self.request:
            self.user = self.request.user

class ShopSerializersMixin(SerializersMixin):
    
    def __init__(self, *args, **kwargs):
        super(ShopSerializersMixin, self).__init__(*args, **kwargs)
        
        self.shop = None
        
        if self.user:
            self.shop = self.request.shop