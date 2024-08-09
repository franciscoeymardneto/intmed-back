from django.contrib.auth.models import User
from rest_framework import serializers


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("first_name", "email", "password", "password2")

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                "Senhas não conferem. Por favor digite senhas iguais."
            )
        if not data.get("email"):
            raise serializers.ValidationError(
                "Email não fornecido, por favor forneça o email"
            )
        if not data.get("first_name"):
            raise serializers.ValidationError(
                "Nome do usuário não fornecido, por favor forneça o nome"
            )
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User()
        user.set_password(validated_data["password"])
        user.username = validated_data["email"]
        user.email = validated_data["email"]
        user.first_name = validated_data["first_name"]
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return user
