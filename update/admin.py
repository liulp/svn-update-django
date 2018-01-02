# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Host, Project, Prohost, Entry
admin.site.register(Host)
admin.site.register(Prohost)
admin.site.register(Project)
admin.site.register(Entry)