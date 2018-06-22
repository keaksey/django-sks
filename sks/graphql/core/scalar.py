'''
Created on Jun 22, 2018

@author: keaksey
'''
from graphene.types import Scalar

class MessagesScalar(Scalar):
    
    @staticmethod
    def parse_literal(node):
        return node.value
    
    @staticmethod
    def parse_value(value):
        return value
    
    @staticmethod
    def serialize(value):
        return value