'''
Created on May 21, 2018

@author: keakseysum
'''
import graphene
from graphene import relay

from graphene_django import DjangoObjectType
from graphene_django.rest_framework.types import ErrorType
from graphene.types import Scalar

class CountableConnection(relay.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int(
        description='A total count of items in the collection')

    @staticmethod
    def resolve_total_count(root, info, *args, **kwargs):
        return root.length

class CountableDjangoObjectType(DjangoObjectType):
    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, *args, **kwargs):
        # Force it to use the countable connection
        countable_conn = CountableConnection.create_type(
            "{}CountableConnection".format(cls.__name__),
            node=cls)
        super().__init_subclass_with_meta__(
            *args, connection=countable_conn, **kwargs)

class MessagesScalar(Scalar):
    
    @staticmethod
    def parse_literal(node):
        return node.value
    
    @staticmethod
    def parse_value(value):
        return value
    
    @staticmethod
    def serialize(value):
        print('value ', value)
        return value

class Error(ErrorType):
    messages = MessagesScalar(required=True)
