from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habit_tracker.models import Habit
from user_account.models import User


class HabitTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="ae215", id_chat_tg="1411676548")
        self.habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="07:10:00",
            action="Зарядка",
            award="Чашка кофе",
            time_to_complete=120,
        )
        self.related_habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="9:10:00",
            action="Принятие ванны",
            time_to_complete=120,
            is_pleasant=True,
        )
        self.habit_two = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="11:10:00",
            action="10 отжиманий",
            time_to_complete=120,
            award="Пряник",
        )
        self.habit_wrong_pleasant = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="11:10:00",
            action="10 отжиманий",
            time_to_complete=120,
            award="Пряник",
            is_pleasant=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_retrieve(self):
        url = reverse("habit_tracker:habit-detail", args=(self.habit.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_create(self):
        url = reverse("habit_tracker:habit-list")
        data = {
            "place": "Спортивная площадка",
            "time": "09:30:00",
            "action": "10 подтягиваний",
            "award": "Конфета",
            "time_to_complete": 120,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_habit_non_field_errors(self):
        url = reverse("habit_tracker:habit-list")
        data = {
            "place": "Спортивная площадка",
            "time": "09:30:00",
            "action": "10 подтягиваний",
            "related_habit": self.related_habit.pk,
            "award": "Конфета",
            "time_to_complete": 120,
        }
        response = self.client.post(url, data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {
                "non_field_errors": [
                    "Нельзя одновременно указывать поле related_habit и поле award."
                ]
            },
        )

    def test_habit_related_one(self):
        url = reverse("habit_tracker:habit-list")
        data = {
            "place": "Работа",
            "time": "07:30:00",
            "action": "Приходить вовремя",
            "related_habit": self.habit.pk,
            "time_to_complete": 50,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {
                "related_habit": [
                    "Связанная привычка должна иметь признак приятной привычки (is_pleasant=True)."
                ]
            },
        )

    def test_habit_related_two(self):
        url = reverse("habit_tracker:habit-list")
        data = {
            "place": "Школа",
            "time": "09:30:00",
            "action": "Обедать",
            "related_habit": self.habit_wrong_pleasant.pk,
            "time_to_complete": 50,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {
                "related_habit": [
                    "У приятной привычки не может быть вознаграждения или связанной привычки."
                ]
            },
        )

    def test_habit_update(self):
        url = reverse("habit_tracker:habit-detail", args=(self.habit.pk,))
        data = {
            "place": "Спортивная площадка",
            "time": "09:30:00",
            "action": "10 подтягиваний",
            "award": "Пирожок",
            "time_to_complete": 120,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_delete(self):
        url = reverse("habit_tracker:habit-detail", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
