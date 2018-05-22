from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import pgettext_lazy, ugettext_lazy as _


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
    
    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email
    
    class Meta:
        permissions = (
            ('view_user',
             pgettext_lazy('Permission description', 'Can view users')),
            ('edit_user',
             pgettext_lazy('Permission description', 'Can edit users')),
            ('view_group',
             pgettext_lazy('Permission description', 'Can view groups')),
            ('edit_group',
             pgettext_lazy('Permission description', 'Can edit groups')),
            ('view_staff',
             pgettext_lazy('Permission description', 'Can view staff')),
            ('edit_staff',
             pgettext_lazy('Permission description', 'Can edit staff')),
            ('impersonate_user',
             pgettext_lazy('Permission description', 'Can impersonate users'))
        )

class Profile(models.Model):
    MALE           = 'M'
    FIMALE         = 'F'
    UNSPECIFIED    = ''
    
    GENDER_CHOICES = (
        (MALE, 'male'),
        (FIMALE, 'fimale'),
        (UNSPECIFIED, 'unspecified')
    )
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        unique=True
    )
    
    about = models.TextField(
        _("about"), 
        blank=True
    )
    
    address  = models.CharField(
        _("address"),
        blank=True,
        max_length=255
    )
    
    phone_number = models.CharField(
        _("Phone number of user"),
        max_length=20,
        blank=True
    )
    
    location = models.CharField(
        _("location"),
        max_length=255, 
        null=True,
        blank=True
    )
    
    website = models.URLField(
        _("website"),
        max_length=255,
        blank=True
    )
    
    gender = models.CharField(
        _("gender"), 
        max_length=2,
        choices=GENDER_CHOICES,
        default=UNSPECIFIED,
        blank=True
    )
    
    def __str__(self):
        return '%s' % self.user
