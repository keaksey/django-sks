'''
Created on May 21, 2018

@author: keakseysum
'''
from collections import OrderedDict

import graphene
from django.core.exceptions import ImproperlyConfigured
from graphene.types.mutation import MutationOptions
from graphene_django.form_converter import convert_form_field
from graphene_django.registry import get_global_registry
from graphql_jwt import ObtainJSONWebToken
from graphql_jwt.exceptions import GraphQLJWTError
from graphql_jwt.decorators import staff_member_required, login_required
from graphene_django.rest_framework.mutation import SerializerMutation as QLSerializer

from ..utils import get_node
from .decorators import permission_required
from .types import Error
from graphene_django.rest_framework.types import ErrorType

registry = get_global_registry()


def convert_form_fields(form_class, exclude=None):
    """Convert form fields to Graphene fields"""
    fields = OrderedDict()
    if exclude is None:
        exclude = []
    for name, field in form_class.base_fields.items():
        if name not in exclude:
            fields[name] = convert_form_field(field)
    return fields


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


class ModelFormMutation(BaseMutation):

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(
            cls, arguments=None, form_class=None, return_field_name=None,
            _meta=None, exclude=None, **options):
        if not form_class:
            raise ImproperlyConfigured(
                'form_class are required for ModelFormMutation')

        _meta = ModelFormMutationOptions(cls)
        model = form_class._meta.model
        if not return_field_name:
            return_field_name = get_model_name(model)
        fields = get_output_fields(model, return_field_name)
        # get mutation arguments based on model form
        arguments = convert_form_fields(form_class, exclude)

        _meta.form_class = form_class
        _meta.model = model
        _meta.return_field_name = return_field_name

        super().__init_subclass_with_meta__(_meta=_meta, **options)

        cls._update_mutation_arguments_and_fields(
            arguments=arguments, fields=fields)

    @classmethod
    def get_form_kwargs(cls, root, info, **input):
        return {'data': input}

    @classmethod
    def mutate(cls, root, info, **kwargs):
        form_kwargs = cls.get_form_kwargs(root, info, **kwargs)
        form = cls._meta.form_class(**form_kwargs)
        if form.is_valid():
            instance = form.save()
            kwargs = {cls._meta.return_field_name: instance}
            return cls(errors=[], **kwargs)
        errors = convert_form_errors(form)
        return cls(errors=errors)


class ModelFormUpdateMutation(ModelFormMutation):

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, *args, **kwargs):
        super().__init_subclass_with_meta__(cls, *args, **kwargs)
        cls._meta.arguments.update({'id': graphene.ID()})

    @classmethod
    def get_form_kwargs(cls, root, info, **input):
        kwargs = super().get_form_kwargs(root, info, **input)
        id = input['id']
        model = cls._meta.form_class._meta.model
        model_type = registry.get_type_for_model(model)
        instance = get_node(info, id, only_type=model_type)
        kwargs['instance'] = instance

        return kwargs


class StaffMemberRequiredMixin(graphene.Mutation):
    permissions = ()

    @classmethod
    @staff_member_required
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
    
    @classmethod
    def get_resp_fields(cls):
        
        if not getattr(cls, 'response_fields'):
            raise 'response_fields is required for the SerializerMutation'
        
        return cls.response_fields
    
    class Meta:
        abstract = True
    
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        serializer = cls._meta.serializer_class(
            data=input, 
            context=dict(request=info.context)
        )
        
        if serializer.is_valid():
            return cls.perform_mutate(serializer, info)
        else:
            errors = [
                ErrorType(field=key, messages=value)
                for key, value in serializer.errors.items()
            ]
            
            return cls(errors=errors)
    
    @classmethod
    def perform_mutate(cls, serializer, info):
        response_fields = cls.get_resp_fields()
        
        obj = serializer.save()
        
        ctx = {}
        for field in response_fields:
            ctx.update(dict(field=getattr(obj, field)))
        
        return cls(errors=None, **ctx)