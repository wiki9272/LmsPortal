from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Project , Task


class UserAdminn(BaseUserAdmin):
    list_display = ["email", "name","role","is_active","job",]
    list_filter = ["role","is_active"]
    fieldsets = [
        ("Credentials", {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name","role",]}),
        ("Permissions", {"fields": ["is_active"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name","role","job", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []

class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name","description","deadline","assigned_by","assigned_on"]
    
class TaskAdmin(admin.ModelAdmin):
    list_display = ["id","project_name","name","details","user","isCompleted","created_at","updated_at"]

# Now register the new UserAdmin...

admin.site.register(User, UserAdminn)
admin.site.register(Project,ProjectAdmin)
admin.site.register(Task,TaskAdmin)