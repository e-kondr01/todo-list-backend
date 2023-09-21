from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from users.models import User
from tasks.models import Task


class HasTaskPermission(IsAuthenticated):
    def has_object_permission(
        self, request: Request, view: ModelViewSet, obj: Task
    ) -> bool:
        user: User = request.user
        is_authenticated = super().has_object_permission(request, view, obj)
        return is_authenticated and obj.user == user
