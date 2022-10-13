import io
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from .models import Category, Report
from src.profiles.models import FatUser


class SupportTests(APITestCase):

    def setUp(self):
        self.user_test1 = FatUser.objects.create_user(
            username='alexey',
            password='pwpk3oJ*T7',
            email='alexey@mail.ru'
        )
        self.user_test1.save()
        self.user_test1_token = Token.objects.create(user=self.user_test1)

        self.category = Category.objects.create(
            id=1,
            name="Ошибка в проверке задания"

        )
        self.report = Report.objects.create(
            category=self.category,
            user=self.user_test1,
            text="Пропала кнопка проверить",
            status="новая"
        )

        image = io.BytesIO()
        Image.new("RGB", (500, 500)).save(image, "JPEG")
        self.image_file = SimpleUploadedFile("image.jpg", image.getvalue())

    def test_get_reports_list(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(reverse("reports"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_reports_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(reverse("reports-detail", kwargs={"pk": self.report.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("text"), "Пропала кнопка проверить")

    def test_creat_report(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        data = {
            "category": 1,
            "user": self.user_test1,
            "text": "Не работает кнопка сдать отчет",
            "status": "новая",
            "image": self.image_file,
        }
        response = self.client.post(reverse("reports"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
