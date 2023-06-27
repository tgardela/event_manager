from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'start_date', 'end_date', 'description',
                    'capacity', 'get_attendees', 'created_by', 'created', 'updated')


admin.site.unregister(Group)

admin.site.site_header = 'Event Manager Admin Panel'
