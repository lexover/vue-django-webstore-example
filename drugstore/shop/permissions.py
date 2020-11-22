from rest_framework import permissions


# Allow only 'GET', 'HEAD', 'OPTIONS' for any.
class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


#  Allow create operation to any user. An all other operations only for authorized user and admin.
class UserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'CREATE':
            return True
        elif request.method in ('GET', 'PUT', 'PATCH'):
            return bool(request.user and (request.user.is_staff or obj == request.user))


# Allow create operation to any user. Get operations only for authorized user (object owner) and all operations
# for admin.
class OrderPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'CREATE':
            return True
        elif request.method == 'GET':
            result = bool(request.user and not request.user.is_anonymous
                          and (request.user.is_staff or obj.owner == request.user))
            return result
        elif request.method in ('PUT', 'PATCH', 'DELETE'):
            return bool(request.user and request.user.is_staff)


