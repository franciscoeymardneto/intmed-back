from django.contrib.auth import authenticate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..serializers import UserLoginResponseSerializer, UserLoginSerializer


@swagger_auto_schema(
    operation_description="Método para acesso ao sistema",
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(type=openapi.TYPE_STRING),
            "password": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=["username", "email", "password", "password2"],
        example={
            "username": "newuser",
            "password": "password123",
        },
    ),
)
@api_view(["POST"])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            return Response(
                UserLoginResponseSerializer(user).data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "message": "Credenciais inválidas! Verifique seu nome de usuário ou senha."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
