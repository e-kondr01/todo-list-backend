from rest_framework.viewsets import ModelViewSet

from tasks.models import Task
from tasks.permissions import HasTaskPermission
from tasks.serializers import TaskSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.none()
    serializer_class = TaskSerializer
    permission_classes = (HasTaskPermission,)

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
