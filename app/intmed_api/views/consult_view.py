from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view

from .consult_list_view import list_consults
from .create_consult_view import create_consult
from .delete_consult_view import delete_consult


@swagger_auto_schema(
    operation_description="Método para listar as consultas. Se clientId for fornecido, lista apenas as consultas daquele cliente. Caso contrário, lista todas as consultas.",
    method="get",
    manual_parameters=[
        openapi.Parameter(
            "clientId",
            openapi.IN_QUERY,
            description="ID do cliente",
            type=openapi.TYPE_INTEGER,
        )
    ],
)
@swagger_auto_schema(
    operation_description="Método para marcar consulta",
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "agenda_id": openapi.Schema(type=openapi.TYPE_INTEGER),
            "cliente_id": openapi.Schema(type=openapi.TYPE_INTEGER),
            "horario": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=["agenda_id", "horario", "cliente_id"],
        example={
            "agenda_id": 1,
            "cliente_id": 2,
            "horario": "13:00",
        },
    ),
)
@api_view(["GET", "POST"])
def consults_view(request):
    if request.method == "GET":
        return list_consults(request)
    elif request.method == "POST":
        return create_consult(request)
