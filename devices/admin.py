from django.contrib import admin

from devices.models import *

# Register your models here.
admin.site.register(Sector)
admin.site.register(Device)
admin.site.register(PowerConsumption)
admin.site.register(Price)
admin.site.register(SectorConsumption)