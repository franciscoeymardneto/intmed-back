from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response

from ..models import Consult, Schedule
from ..serializers import ConsultSerializer, CreateScheduleSerializer


def create_consult(request):
    serializer = CreateScheduleSerializer(data=request.data)
    if serializer.is_valid():
        agenda_id = serializer.validated_data["agenda_id"]
        horario = serializer.validated_data["horario"]
        cliente_id = serializer.validated_data["cliente_id"]

        schedule = Schedule.objects.get(id=agenda_id)

        if not schedule:
            return Response(
                {"error": "Agenda não encontrada."}, status=status.HTTP_400_BAD_REQUEST
            )

        client = User.objects.get(id=cliente_id)

        if not client:
            return Response(
                {"error": "Cliente não encontrado."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            consult = ConsultSerializer(
                Consult.objects.create(schedule=schedule, hour=horario, client=client)
            )
        except ValidationError as e:
            return Response(
                {"error": e.messages.pop()}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            consult.data,
            status=status.HTTP_200_OK,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
