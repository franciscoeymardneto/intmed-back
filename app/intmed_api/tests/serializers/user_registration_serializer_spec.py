from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from ...serializers import UserRegistrationSerializer


class UserRegistrationSerializerTestSuit(TestCase):
    def test_passwords_do_not_match(self):
        data = {
            "first_name": "Test",
            "email": "testuser@example.com",
            "password": "testpassword",
            "password2": "differentpassword",
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(
            serializer.errors["non_field_errors"][0],
            "Senhas não conferem. Por favor digite senhas iguais.",
        )

    def test_passwords_match(self):
        data = {
            "first_name": "Test",
            "email": "testuser@example.com",
            "password": "testpassword",
            "password2": "testpassword",
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_create_user(self):
        data = {
            "first_name": "Test",
            "email": "testuser@example.com",
            "password": "testpassword",
            "password2": "testpassword",
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertEqual(user.username, data["email"])
        self.assertEqual(user.email, data["email"])
        self.assertEqual(user.first_name, data["first_name"])
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password(data["password"]))

    def test_create_user_without_required_fields(self):
        data = {
            "first_name": "Test",
            "password": "testpassword",
            "password2": "testpassword",
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(
            serializer.errors["non_field_errors"][0],
            "Email não fornecido, por favor forneça o email",
        )

        data = {
            "email": "testuser@example.com",
            "password": "testpassword",
            "password2": "testpassword",
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(
            serializer.errors["non_field_errors"][0],
            "Nome do usuário não fornecido, por favor forneça o nome",
        )
