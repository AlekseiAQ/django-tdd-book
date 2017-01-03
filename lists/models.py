from django.db import models


class Item(models.Model):
    """docstring for Item"""
    text = models.TextField(default='')
