from rest_framework import status
from rest_framework.test import APITestCase

from tasks.models import Task
from users.models import User


class TaskTests(APITestCase):
    BASE_URL = "/api"
    TASKS_URL = BASE_URL + "/tasks/"
    TASK_DETAIL_URL = TASKS_URL + "{id}/"

    def setUp(self):
        """
        Создаём пользователя для запросов
        """
        self.user: User = User.objects.create_user(
            email="test@test.com", password="testpassword"
        )
        response = self.client.post(
            "/api/auth/jwt/create/",
            {"email": self.user.email, "password": "testpassword"},
        )
        # Authenticate all test requests
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])

    def test_unauthenticated_requests(self):
        """
        Неавторизованные запросы не должны проходить
        """
        # Stop including any credentials
        self.client.credentials()
        data = {"name": "Task 1"}
        response = self.client.post(self.TASKS_URL, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(self.TASKS_URL, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(self.TASK_DETAIL_URL.format(id=1), format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(
            self.TASK_DETAIL_URL.format(id=1), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(
            self.TASK_DETAIL_URL.format(id=1), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(self.TASK_DETAIL_URL.format(id=1), format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_task(self):
        """
        Возможность создать задачу
        """
        data = {"name": "Task 1"}
        response = self.client.post(self.TASKS_URL, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().name, "Task 1")
        self.assertEqual(Task.objects.get().user, self.user)

    def test_update_task(self):
        """
        Возможность обновить задачу
        """
        data = {"name": "Task 1"}
        response = self.client.post(self.TASKS_URL, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        created_task = Task.objects.get()
        self.assertEqual(created_task.name, "Task 1")
        self.assertEqual(created_task.user, self.user)

        updated_data = {"name": "Task 1 updated"}
        response = self.client.patch(
            self.TASK_DETAIL_URL.format(id=created_task.id), updated_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().name, "Task 1 updated")
        self.assertEqual(Task.objects.get().user, self.user)

    def test_delete_task(self):
        """
        Возможность удалить задачу
        """
        data = {"name": "Task 1"}
        response = self.client.post(self.TASKS_URL, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        created_task = Task.objects.get()

        response = self.client.delete(self.TASK_DETAIL_URL.format(id=created_task.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_can_get_only_own_tasks(self):
        """
        Пользователь может получать только свои задачи в списке
        """
        data = {"name": "Task 1"}
        response = self.client.post(self.TASKS_URL, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.latest("created_at").user, self.user)
        data = {"name": "Task 2"}
        response = self.client.post(self.TASKS_URL, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.latest("created_at").user, self.user)

        user_2: User = User.objects.create_user(
            email="test2@test.com", password="testpassword"
        )
        response = self.client.post(
            "/api/auth/jwt/create/",
            {"email": user_2.email, "password": "testpassword"},
        )
        # Authenticate as user_2
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])
        data = {"name": "Task 3"}
        response = self.client.post(self.TASKS_URL, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_2_task = Task.objects.latest("created_at")
        self.assertEqual(user_2_task.user, user_2)
        self.assertEqual(Task.objects.count(), 3)

        response = self.client.get(self.TASKS_URL).json()
        self.assertEqual(len(response["results"]), 1)
        self.assertEqual(response["results"][0]["name"], "Task 3")
