from django.contrib import admin

from .models import Arduino_Temperature, AdminMongoDB, AdminMySQLDB

# Register your models here.
admin.site.register(Arduino_Temperature, AdminMongoDB)


# admin.site.register(Arduino_Temperature, AdminMySQLDB)
