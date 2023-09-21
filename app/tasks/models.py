from django.db import models

from users.models import User


class Task(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")

    description = models.TextField(verbose_name="Описание", blank=True)

    due_at = models.DateTimeField(
        verbose_name="Дата и время выполнения", blank=True, null=True
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Пользователь",
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время создания"
    )

    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата и время обновления"
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["-due_at", "-created_at"]
