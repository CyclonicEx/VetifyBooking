from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['pet_name', 'owner_name', 'service', 'date', 'time', 'user']
    list_filter = ['service', 'date', 'pet_type']
    search_fields = ['pet_name', 'owner_name', 'email']
    date_hierarchy = 'date'
