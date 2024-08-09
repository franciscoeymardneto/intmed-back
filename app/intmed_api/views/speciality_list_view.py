from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import Speciality
from ..serializers import SpecialitySerializer


@swagger_auto_schema(
    operation_description="Método para listar todas as especialidades", method="get"
)
@api_view(["GET"])
def list_speciality(request):
    specialities = Speciality.objects.all()
    serializer = SpecialitySerializer(specialities, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
