from rest_framework.permissions import SAFE_METHODS, BasePermission


class CommonPermission(BasePermission):
    message = 'Вы не авторизованы на данный запрос'


class IsAdmin(CommonPermission):

    def is_admin(self, user):
        return user.is_authenticated and user.is_admin

    def has_permission(self, request, view):
        return self.is_admin(request.user)

    def has_object_permission(self, request, view, obj):
        return self.is_admin(request.user)


class IsModerator(CommonPermission):

    def is_moderator(self, user):
        return user.is_authenticated and user.is_moderator

    def has_permission(self, request, view):
        return self.is_moderator(request.user)

    def has_object_permission(self, request, view, obj):
        return self.is_moderator(request.user)


class IsAuthor(CommonPermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author


class ReadOnly(CommonPermission):

    def safe_methods(self, request):
        return request.method in SAFE_METHODS

    def has_permission(self, request, view):
        return self.safe_methods(request)

    def has_object_permission(self, request, view, obj):
        return self.safe_methods(request)
