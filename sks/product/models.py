from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator

from django.urls import reverse
from django.contrib.postgres.fields import HStoreField
from django.utils.translation import pgettext_lazy, ugettext_lazy as _

from ..seo.models import SeoModel
from ..users.models import User
from ..shop.models import Shop
from ..core.models import SortableModel

MAX_LENGTH_HADLE_FIELD = 256

PUBLICATION_CHOICES = (
    ('pos', _('Online shop')),
)

class Category(SeoModel):
    name   = models.CharField(max_length=MAX_LENGTH_HADLE_FIELD)
    handle = models.SlugField(max_length=MAX_LENGTH_HADLE_FIELD)
    description = models.TextField(blank=True)
    
    shop = models.ForeignKey(Shop, related_name='categories', on_delete=models.CASCADE)
    
    #tree = TreeManager()

    class Meta:
        app_label = 'product'
        permissions = (
            ('view_category',
             pgettext_lazy('Permission description', 'Can view categories')),
            ('edit_category',
             pgettext_lazy('Permission description', 'Can edit categories')))
        unique_together = ('shop', 'handle', )
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self, ancestors=None):
        return reverse('product:category',
                       kwargs={'path': self.get_full_path(ancestors),
                               'category_id': self.id})
        
class ProductType(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_HADLE_FIELD)
    handle = models.SlugField(max_length=MAX_LENGTH_HADLE_FIELD)
    description = models.TextField(blank=True)
    
    shop = models.ForeignKey(Shop, related_name='product_types', on_delete=models.CASCADE)
    
    class Meta:
        app_label = 'product'
        permissions = (
            ('view_product_type',
             pgettext_lazy('Permission description', 'Can view product_types')),
            ('edit_product_type',
             pgettext_lazy('Permission description', 'Can edit product_types')))
        
        unique_together = ('shop', 'handle', )
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        class_ = type(self)
        return '<%s.%s(pk=%r, name=%r)>' % (
            class_.__module__, class_.__name__, self.pk, self.name)

class Product(SeoModel):
    product_type = models.ForeignKey(
        ProductType, related_name='products', on_delete=models.CASCADE)
    
    shop = models.ForeignKey(Shop, related_name='products', on_delete=models.CASCADE)
    
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    
    user = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name='products'
    )
    
    body_html = models.TextField(_('description'), blank=True)
    
    handle = models.CharField(
        _('handle'), 
        max_length=MAX_LENGTH_HADLE_FIELD
    )
    
    published_at = models.DateTimeField(null=True)
    
    published_scope = models.CharField(max_length=64, default='global')
    
    updated_at = models.DateTimeField(
        _('updated at'),
        auto_now=True
    )
    
    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True
    )
    
    published_scope = models.CharField(
        _('visability'), 
        choices=PUBLICATION_CHOICES,
        default="pos",
        max_length=30
    )
    
    attributes = HStoreField(default={}, blank=True)
    
    class Meta:
        app_label = 'product'
        permissions = (
            ('view_product',
             pgettext_lazy('Permission description', 'Can view products')),
            ('edit_product',
             pgettext_lazy('Permission description', 'Can edit products')))
            
        unique_together = ('shop', 'handle', )
        
    def __iter__(self):
        if not hasattr(self, '__variants'):
            setattr(self, '__variants', self.variants.all())
        return iter(getattr(self, '__variants'))
    
    def __repr__(self):
        class_ = type(self)
        return '<%s.%s(pk=%r, name=%r)>' % (
            class_.__module__, class_.__name__, self.pk, self.name)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse(
            'product:details',
            kwargs={'slug': self.get_slug(), 'product_id': self.id})
        
class ProductVariant(SortableModel):
    
    product = models.ForeignKey(
        Product, related_name='variants', on_delete=models.CASCADE)
    
    attributes = HStoreField(default={}, blank=True)
    
    inventory_management = models.CharField(
        max_length=32, 
        blank=True,
        default='blank'
    ) 
    
    inventory_policy = models.CharField(
        max_length=32, 
        blank=True,
        default='deny'
    )
    
    quantity = models.IntegerField(
        validators=[MinValueValidator(0)], 
        default=Decimal(1)
    )
    
    quantity_allocated = models.IntegerField(
        validators=[MinValueValidator(0)], default=Decimal(0))
    
    option1 = models.CharField(blank=True, default='', max_length=MAX_LENGTH_HADLE_FIELD)
    option2 = models.CharField(blank=True, default='', max_length=MAX_LENGTH_HADLE_FIELD)
    option3 = models.CharField(blank=True, default='', max_length=MAX_LENGTH_HADLE_FIELD)
    
    position = models.IntegerField(null=True, default=1)
    
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )
    
    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    
    sku = models.CharField(blank=True, default='', max_length=MAX_LENGTH_HADLE_FIELD)
    
    class Meta:
        app_label = 'product'
        ordering = ('position', )
        
    def get_ordering_queryset(self):
        return self.product.values.all()
    