'''
Created on May 21, 2018

@author: keakseysum
'''

import graphene
from django.core.exceptions import ImproperlyConfigured
from graphene.types.mutation import MutationOptions
from graphene_django.registry import get_global_registry
from graphql_jwt import ObtainJSONWebToken
from graphql_jwt.exceptions import GraphQLJWTError
from graphql_jwt.decorators import login_required
from graphene_django.rest_framework.mutation import SerializerMutation as QLSerializer

from ..utils import get_node
from .decorators import permission_required
from .types import Error

registry = get_global_registry()

def convert_form_errors(form):
    """Convert ModelForm errors into a list of Error objects."""
    errors = []
    for field in form.errors:
        for message in form.errors[field]:
            errors.append(Error(field=field, message=message))
    return errors

def get_model_name(model):
    """Return name of the model with first letter lowercase."""
    model_name = model.__name__
    return model_name[:1].lower() + model_name[1:]


def get_output_fields(model, return_field_name):
    """Return mutation output field for model instance."""
    model_type = registry.get_type_for_model(model)
    fields = {return_field_name: graphene.Field(model_type)}
    return fields


class BaseMutation(graphene.Mutation):
    errors = graphene.List(
        Error,
        description='List of errors that occurred executing the mutation.')

    class Meta:
        abstract = True

    @classmethod
    def _update_mutation_arguments_and_fields(cls, arguments, fields):
        cls._meta.arguments.update(arguments)
        cls._meta.fields.update(fields)


class ModelFormMutationOptions(MutationOptions):
    form_class = None
    return_field_name = None


class ModelDeleteMutationOptions(MutationOptions):
    model = None
    return_field_name = None


class ModelDeleteMutation(BaseMutation):

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(
            cls, arguments=None, model=None, return_field_name=None,
            _meta=None, **options):
        if not model:
            raise ImproperlyConfigured(
                'model is required for ModelDeleteMutation')

        _meta = ModelDeleteMutationOptions(cls)

        if not return_field_name:
            return_field_name = get_model_name(model)
        if arguments is None:
            arguments = {}
        arguments.update({'id': graphene.ID()})
        fields = get_output_fields(model, return_field_name)

        _meta.model = model
        _meta.return_field_name = return_field_name

        super().__init_subclass_with_meta__(_meta=_meta, **options)

        # Update mutation's arguments and fields
        cls._update_mutation_arguments_and_fields(
            arguments=arguments, fields=fields)

    @classmethod
    def mutate(cls, root, info, id, **kwargs):
        model = cls._meta.model
        model_type = registry.get_type_for_model(model)
        instance = get_node(info, id, only_type=model_type)
        instance.delete()
        field_name = cls._meta.return_field_name
        kwargs = {field_name: instance}
        return cls(**kwargs)

class StaffMemberRequiredMixin(graphene.Mutation):
    permissions = ()
    
    @classmethod
#     @staff_member_required
    def mutate(cls, root, info, *args, **kwargs):
        mutate = permission_required(cls.permissions)(super().mutate)
        return mutate(root, info, *args, **kwargs)

class LoginRequiredMixin(graphene.Mutation):
    
    @classmethod
    @login_required
    def mutate(cls, root, info, *args, **kwargs):
        return super().mutate(root, info, *args, **kwargs)
    
class CreateToken(ObtainJSONWebToken):
    """Mutation that authenticates a user and returns token.

    It overrides the default graphql_jwt.ObtainJSONWebToken to wrap potential
    authentication errors in our Error type, which is consistent to how rest of
    the mutation works.
    """

    errors = graphene.List(Error)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        try:
            result = super().mutate(root, info, **kwargs)
        except GraphQLJWTError as e:
            return CreateToken(errors=[Error(message=str(e))])
        else:
            return result
    
class SerializerMutation(QLSerializer):
    
    errors = graphene.List(
        Error,
        description='May contain more than one error for same field.'
    )
    
    class Meta:
        abstract = True
        
class ShopSerializerMutation(SerializerMutation):
    
    class Input:
        shop = graphene.String()
    
    class Meta:
        abstract = True
