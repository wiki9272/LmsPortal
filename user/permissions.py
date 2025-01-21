from rest_framework.permissions import BasePermission

class IsActive(BasePermission):
    def has_permission(self, request):
            print(request)
            return request