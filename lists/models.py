from django.db import models


class List(models.Model):
    """docstring for List"""
    pass


class Item(models.Model):
    """docstring for Item"""
    text = models.TextField(default='')
    list = models.ForeignKey(List, default='')

