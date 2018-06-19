'''
Created on Jun 19, 2018

@author: keakseysum
'''
from django_filters import OrderingFilter
from collections import OrderedDict
from django.utils.translation import pgettext_lazy

from ..core.filters import DistinctFilterSet
from ...product import models

SORT_BY_FIELDS = OrderedDict([
    ('name', pgettext_lazy('Product list sorting option', 'name')),
    ('price', pgettext_lazy('Product list sorting option', 'price'))])

class ProductFilterSet(DistinctFilterSet):
    sort_by = OrderingFilter(
        fields=SORT_BY_FIELDS.keys(), field_labels=SORT_BY_FIELDS)

    class Meta:
        model = models.Product
        fields = {
            'category': ['exact'],
            'price': ['exact', 'range', 'lte', 'gte'],
            'name': ['exact', 'icontains'],
            'product_type__name': ['exact'],
            'is_published': ['exact']}
    
    @classmethod
    def filter_for_field(cls, f, field_name, lookup_expr='exact'):
#         if field_name == 'attributes':
#             return ProductAttributeFilter(
#                 field_name=field_name, lookup_expr=lookup_expr, distinct=True)
        # this class method is called during class construction so we can't
        # reference ProductFilterSet here yet
        # pylint: disable=E1003
        return super(DistinctFilterSet, cls).filter_for_field(
            f, field_name, lookup_expr)
        