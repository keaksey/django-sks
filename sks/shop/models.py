from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import pgettext_lazy, ugettext_lazy as _
from django.contrib.sites.models import Site

from ..seo.models import SeoModel
from ..users.models import User

# Create your models here.
PLAN_CHOICES = (
    ('trial', _('Trail')),
    ('affiliate', _('Trial from Partner')),
    ('basic', _('Basic Shopify')),
    ('professional', _('Shopify')),
    ('unlimited', _('Advanced Shopify')),
    ('enterprise', _('Shopify Plus')),
)

USER_TYPES = (
    ('cashier', _('Cashier')),
    ('manager', _('Manager')),
    ('waiter', _('A person that can order')),
    ('admin', _('Shop owner'))
)

class ShopStaff(models.Model):
    username_validator = UnicodeUsernameValidator()
    
    shop = models.ForeignKey('Shop', related_name='shop_staff', on_delete=models.CASCADE)
    
    user  = models.ForeignKey(User, related_name='shop_staff', on_delete=models.CASCADE)
    
    last_login = models.DateTimeField(
        _('created at'),
        null=True
    )
    
    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    
    is_owner = models.BooleanField(default=False)
    
    class Meta:
        app_label = 'shop'
        permissions = (
            ('edit_staff',
             pgettext_lazy('Permission description',
                           'Can edit staff')),
            ('view_staff',
             pgettext_lazy('Permission description',
                           'Can view staff')))
        
    
class Shop(SeoModel):
    site = models.OneToOneField(
        Site, related_name='settings', on_delete=models.CASCADE)
    
    name = models.CharField(
        _('name'), 
        db_index=True,
        max_length=256
    )
    
    staff = models.ManyToManyField(
        User,
        through='ShopStaff'
    )
    
    class Meta:
        app_label = "shop"
        
        permissions = (
            ('edit_shop',
             pgettext_lazy('Permission description',
                           'Can edit staff')),
            ('view_shop',
             pgettext_lazy('Permission description',
                           'Can view staff')))
        