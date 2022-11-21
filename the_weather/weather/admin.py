from django.contrib import admin

from .models import AdminMongoDB, AdminMySQLDB,  TemperatureCity

# Register your models here


# admin.site.register(TemperatureCity, AdminMongoDB)

admin.site.register(TemperatureCity, AdminMySQLDB)
