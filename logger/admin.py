from django.contrib import admin
from .models import User ,Project, Log

class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('name','total_hours')


admin.site.register(User)
admin.site.register(Project,ProjectsAdmin)
admin.site.register(Log)
