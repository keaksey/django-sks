from django.contrib.auth.models import Permission

MODELS_PERMISSIONS = [
    'user.view_user',
    'user.edit_user',
    'user.view_group',
    'user.edit_group',
    'user.view_staff',
    'user.edit_staff',
    'user.impersonate_user'
]

def get_permissions():
    codenames = [permission.split('.')[1] for permission in MODELS_PERMISSIONS]
    return Permission.objects.filter(codename__in=codenames)\
        .prefetch_related('content_type')