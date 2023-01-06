from django.contrib import admin

from . import models


admin.site.register(models.Group)
admin.site.register(models.GroupMember)
admin.site.register(models.GroupMessage)
admin.site.register(models.PV)
admin.site.register(models.PVMessage)