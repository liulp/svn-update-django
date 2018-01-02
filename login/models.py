# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model): #用户
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=1024)
    email = models.EmailField()
    mobile = models.CharField(max_length=13)

    def __unicode__(self):
        return self.username