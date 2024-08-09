import hashlib

from django.contrib.auth.models import User
from django.test import TestCase

from ...serializers import UserLoginResponseSerializer, UserLoginSerializer


class UserLoginSerializerTestSuit(TestCase):
    def test_valid_data(self):
        # Testa a validação de dados válidos
        data = {"username": "testuser", "password": "testpassword"}
        serializer = UserLoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, data)

    def test_invalid_data(self):
        # Testa a validação de dados inválidos (faltando password)
        data = {"username": "testuser"}
        serializer = UserLoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)


class UserLoginResponseSerializerTestSuit(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            first_name="Test",
            last_name="User",
            email="testuser@intmed.com",
        )

    def test_serialization(self):
        # Testa a serialização do usuário
        serializer = UserLoginResponseSerializer(instance=self.user)
        data = serializer.data
        self.assertEqual(data["username"], "Test")

        # Testa o campo token
        expected_token_string = f"{self.user.username}{self.user.email}"
        expected_token_hash = hashlib.sha256(expected_token_string.encode()).hexdigest()
        self.assertEqual(data["token"], expected_token_hash)

        # Testa o campo id
        self.assertEqual(data["userid"], self.user.id)

    def test_get_username(self):
        serializer = UserLoginResponseSerializer(instance=self.user)
        username = serializer.get_username(self.user)
        self.assertEqual(username, "Test")

    def test_get_token(self):
        serializer = UserLoginResponseSerializer(instance=self.user)
        token = serializer.get_token(self.user)
        expected_token_string = f"{self.user.username}{self.user.email}"
        expected_token_hash = hashlib.sha256(expected_token_string.encode()).hexdigest()
        self.assertEqual(token, expected_token_hash)

    def test_get_userid(self):
        serializer = UserLoginResponseSerializer(instance=self.user)
        userid = serializer.get_userid(self.user)
        self.assertEqual(userid, self.user.id)
