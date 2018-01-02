# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from login.models import User
# Create your models here.

ASSET_TYPE = (
    ("L", "linux"),
    ("W", "windows")
    )


class Host(models.Model):
    ip = models.GenericIPAddressField(max_length=15, unique=True)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=1024)
    port = models.IntegerField()
    type = models.CharField(choices=ASSET_TYPE, max_length=30)

    def __unicode__(self):
        return "%s, %s" % (self.ip, self.type)


class Project(models.Model):
    program = models.CharField(max_length=50)
    svn_path = models.CharField(max_length=1024)
    src_path = models.CharField(max_length=1024)
    propath = models.TextField(max_length=2048)

    def __unicode__(self):
        return "%s, %s, %s, %s" % (self.program, self.svn_path, self.src_path, self.propath)

class Prohost(models.Model):
    host = models.ForeignKey(Host)
    dest_path = models.CharField(max_length=1024)
    project = models.ForeignKey(Project)

    def __unicode__(self):
        return "%s, %s, %s" % (self.host, self.dest_path, self.project)

class Entry(models.Model):
    date = models.DateTimeField()
    user = models.ForeignKey(User)
    item = models.CharField(max_length=1024)
    project = models.ForeignKey(Project)

    def __unicode__(self):
        return "%s, %s, %s, %s" % (self.date, self.user, self.item, self.project)

class Rollback(models.Model):
    date = models.DateTimeField()
    user = models.ForeignKey(User)
    item = models.CharField(max_length=1024)
    project = models.ForeignKey(Project)
    rolldate = models.DateTimeField()

    def __unicode__(self):
        return "%s, %s, %s, %s, %s" % (self.date, self.user, self.item, self.project, self.rolldate)









