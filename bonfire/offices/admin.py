from django.contrib import admin

from . import models


@admin.register(models.Office)
class OfficeAdmin(admin.ModelAdmin):
    pass
