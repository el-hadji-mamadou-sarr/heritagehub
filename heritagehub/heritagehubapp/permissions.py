from rest_framework.permissions import BasePermission

class IsGetRequest(BasePermission):
    def has_permission(self, request, view):
        return request.method == 'GET'