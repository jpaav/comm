from django.contrib import admin

from patientlog.models import Tag, Entry, Log, Resident

admin.site.register(Tag)

admin.site.register(Entry)

admin.site.register(Log)

admin.site.register(Resident)
