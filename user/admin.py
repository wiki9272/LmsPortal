from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Project , Task, Client


class UserAdminn(BaseUserAdmin):
    list_display = ["email", "name","role","is_active","job"]
    # def display_project_assigned(self, obj):
    #     return ", ".join([project.name for project in obj.projects_assigned.all()])
    
    # display_project_assigned.short_description = 'Projects Assigned'
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
    list_display = ["name","description","deadline","assigned_by","assigned_on","display_assigned", "client"]

    def display_assigned(self, obj):
        return ", ".join([user.name for user in obj.assigned_to.all()])
    
    display_assigned.short_description = 'Assigned To'
    
class TaskAdmin(admin.ModelAdmin):
    list_display = ["id","project_name","name","details","user","isCompleted","created_at","updated_at","flag"]

class ClientAdmin(admin.ModelAdmin):
    list_display = ["name","email","details"]

# Now register the new UserAdmin...

admin.site.register(User, UserAdminn)
admin.site.register(Project,ProjectAdmin)
admin.site.register(Task,TaskAdmin)
admin.site.register(Client, ClientAdmin)