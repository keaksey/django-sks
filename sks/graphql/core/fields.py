'''
Created on Jun 20, 2018

@author: keaksey
'''
from graphene import Field
from functools import partial
# from graphene_django.utils import maybe_queryset

class DjangoObjectField(Field):
    
    def __init__(self, _type, *args, **kwargs):
        super(DjangoObjectField, self).__init__(_type, *args, **kwargs)

    @property
    def model(self):
        return self.type.of_type._meta.node._meta.model

    @staticmethod
    def object_resolver(resolver, root, info, **args):
        return resolver.objects.filter(**args).get()
    
    def get_resolver(self, parent_resolver):
        return partial(
            self.object_resolver,
            self.type._meta.model
        )