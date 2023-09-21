import django_filters

from tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    order_by = django_filters.OrderingFilter(
        fields=(
            ("due_at", "due_at"),
            ("created_at", "created_at"),
            ("priority", "priority"),
        )
    )

    class Meta:
        model = Task
        fields = {
            "name": ["icontains"],
            "due_at": ["exact", "gte", "lte"],
            "is_completed": ["exact"],
            "priority": ["exact"],
        }
