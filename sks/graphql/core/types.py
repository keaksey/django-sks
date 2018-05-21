'''
Created on May 21, 2018

@author: keakseysum
'''
import graphene
from graphene_django import DjangoObjectType


class CountableConnection(graphene.relay.Connection):
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


class Error(graphene.ObjectType):
    field = graphene.String(
        description="""Name of a field that caused the error. A value of
        `null` indicates that the error isn't associated with a particular
        field.""", required=False)
    message = graphene.String(description='The error message.')

    class Meta:
        description = 'Represents an error in the input of a mutation.'
