from django.core.exceptions import ValidationError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import Consult


@swagger_auto_schema(
    operation_description="Método para desmarcar uma consulta",
    method="delete",
    manual_parameters=[
        openapi.Parameter(
            "consulta_id",
            openapi.IN_PATH,
            description="ID da consulta",
            type=openapi.TYPE_INTEGER,
        )
    ],
)
@api_view(["DELETE"])
def delete_consult(request, consulta_id):
    try:
        consult = Consult.objects.get(id=consulta_id)
    except Consult.DoesNotExist:
        return Response(
            {
                "error": "Não foi possível desmarcar a consulta. Consulta não encontrada."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        consult.delete()
        return Response(status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"error": e.messages.pop()}, status=status.HTTP_400_BAD_REQUEST)
