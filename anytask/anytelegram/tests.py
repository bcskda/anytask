from django.test import TestCase

from users.models import User, UserProfile
from common import AnyTelegram


class AnyTelegramTests(TestCase):
    def setUp(self):
        super(AnyTelegramTests, self).setUpClass()
        self.api = AnyTelegram()
        self.first_student = User.objects.create_user(
            username='first_student', password='password')
        self.second_student = User.objects.create_user(
            username='second_student', password='password')

    def test_non_null_link_secret(self):
        self.assertIsNotNone(self.first_student.profile.telegram_link_secret)
        self.assertIsNotNone(self.second_student.profile.telegram_link_secret)

    def test_unique_link_secret(self):
        self.assertNotEqual(
            self.first_student.profile.telegram_link_secret,
            self.second_student.profile.telegram_link_secret
        )
