from django.contrib import admin

from patientlog.models import Tag, Entry, Log

admin.site.register(Tag)

admin.site.register(Entry)

admin.site.register(Log)
