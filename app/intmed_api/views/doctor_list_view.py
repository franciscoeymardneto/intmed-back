from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import Doctor
from ..serializers import DoctorSerializer


@swagger_auto_schema(
    operation_description="Método para listar os médicos. Se specialityId for fornecido, \
        lista apenas os médicos daquela especialidade. Caso contrário, lista todos os médicos.",
    method="get",
    manual_parameters=[
        openapi.Parameter(
            "specialityId",
            openapi.IN_QUERY,
            description="ID da especialidade",
            type=openapi.TYPE_INTEGER,
        )
    ],
)
@api_view(["GET"])
def list_doctors(request):
    speciality_id = request.query_params.get("specialityId", None)

    if speciality_id:
        doctors = Doctor.objects.filter(speciality__id=speciality_id)
    else:
        doctors = Doctor.objects.all()

    serializer = DoctorSerializer(doctors, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
