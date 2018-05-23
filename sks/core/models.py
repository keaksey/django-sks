'''
Created on May 23, 2018

@author: keakseysum
'''
from django.db import models
from django.db.models import F, Max

class SortableModel(models.Model):
    position = models.PositiveIntegerField(editable=False, db_index=True)

    class Meta:
        abstract = True
    
    def get_ordering_queryset(self):
        raise NotImplementedError('Unknown ordering queryset')

    def save(self, *args, **kwargs):
        if self.position is None:
            qs = self.get_ordering_queryset()
            existing_max = qs.aggregate(Max('position'))
            existing_max = existing_max.get('position__max')
            self.position = 0 if existing_max is None else existing_max + 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        qs = self.get_ordering_queryset()
        qs.filter(sort_order__gt=self.position).update(
            sort_order=F('position') - 1)
        super().delete(*args, **kwargs)