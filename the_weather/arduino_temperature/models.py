from django.db import models
from django.contrib import admin

# Create your models here


class AdminMongoDB(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = 'default'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


class AdminMySQLDB(AdminMongoDB):
    # A handy constant for the name of the alternate database.
    using = 'mysql_db'


class Arduino_Temperature(models.Model):
    id = models.BigIntegerField(primary_key=True)
    created_at = models.DateTimeField(null=True)
    temperature = models.FloatField(null=True)
    humidity = models.FloatField(null=True)

    # def __init__(self, id, created_at, temperature, humidity):
    #     self.id = id
    #     self.created_at = created_at
    #     self.temperature = temperature
    #     self.humidity = humidity
