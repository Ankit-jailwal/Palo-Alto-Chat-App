from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.utils import timezone


class IsAuthenticatedCustom(BasePermission):

    def has_permission(self, request, view):
        from user_auth.views import decodeJWT
        user = decodeJWT(request.META['HTTP_AUTHORIZATION'])
        if not user:
            return False
        request.user = user
        if request.user and request.user.is_authenticated:
            from user_auth.models import CustomUser
            CustomUser.objects.filter(id=request.user.id).update(
                is_online=timezone.now())
            return True
        return False