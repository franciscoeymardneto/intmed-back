import hashlib

from django.contrib.auth.models import User
from rest_framework import serializers


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserLoginResponseSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    userid = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["username", "token", "userid"]

    def get_username(self, obj):
        return obj.first_name

    def get_userid(self, obj):
        return obj.id

    def get_token(self, obj):
        token_string = f"{obj.username}{obj.email}"
        token_hash = hashlib.sha256(token_string.encode()).hexdigest()
        return token_hash
