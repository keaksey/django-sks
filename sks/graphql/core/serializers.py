'''
Created on Jun 7, 2018

@author: keakseysum
'''
class SerializersMixin(object):
    
    def __init__(self, *args, **kwargs):
        super(SerializersMixin, self).__init__(*args, **kwargs)
        self.request = self.context.get('request')
    