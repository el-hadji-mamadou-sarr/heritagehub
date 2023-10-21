from rest_framework.permissions import BasePermission

class IsGetRequest(BasePermission):
    def has_permission(self, request, view):
        return request.method == 'GET'
    
class IsAnonymeUser(BasePermission):
    def has_permission(self, request, view):
        return request.method == 'POST'
    
class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return  request.user.is_superuser 