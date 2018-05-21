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
        