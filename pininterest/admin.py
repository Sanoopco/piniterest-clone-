from django.contrib import admin
from pininterest import models
# Register your models here.
admin.site.register(models.Post)
admin.site.register(models.Follow)