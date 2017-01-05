from django.db import models
from django.core.urlresolvers import reverse

class List(models.Model):
    """docstring for List"""
    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])


class Item(models.Model):
    """docstring for Item"""
    text = models.TextField(default='')
    list = models.ForeignKey(List, default='')

