from rest_framework.permissions import BasePermission

class IsGetRequest(BasePermission):
    def has_permission(self, request, view):
        return request.method == 'GET'
    
class CanCreateUser(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated 
    
class CanListUsers(BasePermission):
    def has_permission(self, request, view):
        return  request.user.is_superuser 