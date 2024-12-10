from django.contrib import admin

# Register your models here.
from .models import Assignment, Profile

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'class_name', 'assigned_to', 'due_date', 'completed')
    list_filter = ('completed', 'class_name')
    search_fields = ('title', 'assigned_to__email')

admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Profile)