from rest_framework import permissions

class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):

        try:
            if request.user.role in ["1","2"]:
                return True
            return False
        except:
            return False