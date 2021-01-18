from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Student)
admin.site.register(User)
admin.site.register(Room)
admin.site.register(Hostel)
admin.site.register(Warden)

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ['student', 'start_date', 'end_date',
                    'reason', 'accept', 'reject', 'confirm_time']

@admin.register(created_date)
class created(admin.ModelAdmin):
    list_display = ['user','created_date']
