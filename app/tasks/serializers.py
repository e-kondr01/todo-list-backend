from rest_framework import serializers

from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Task
        fields = (
            "id",
            "name",
            "description",
            "due_at",
            "user",
            "is_completed",
            "priority",
            "created_at",
            "updated_at",
        )
