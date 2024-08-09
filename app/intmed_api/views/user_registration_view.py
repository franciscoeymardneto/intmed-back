from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..serializers import UserRegistrationSerializer


@swagger_auto_schema(
    operation_description="Cria um novo usuário com acesso ao admin, \
        mas sem privilégios de superadmin.",
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "first_name": openapi.Schema(type=openapi.TYPE_STRING),
            "email": openapi.Schema(
                type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL
            ),
            "password": openapi.Schema(type=openapi.TYPE_STRING),
            "password2": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=["first_name", "email", "password", "password2"],
        example={
            "first_name": "Jhon Due",
            "email": "newuser@example.com",
            "password": "password123",
            "password2": "password123",
        },
    ),
)
@api_view(["POST"])
def createUser(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
