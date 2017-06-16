from django.contrib import admin

from .models import Donor, Recipient, Ngos
# Register your models here.

admin.site.register(Donor)
admin.site.register(Recipient)
admin.site.register(Ngos)