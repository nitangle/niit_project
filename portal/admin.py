from django.contrib import admin

from .models import Donor, Recipient, Ngo, PeopleHelped
# Register your models here.

admin.site.register(Donor)
admin.site.register(Recipient)
admin.site.register(Ngo)
admin.site.register(PeopleHelped)