from rest_framework import serializers

from ..models import Consult
from .doctor_serializer import DoctorSerializer


class ConsultSerializer(serializers.ModelSerializer):
    dia = serializers.SerializerMethodField()
    horario = serializers.SerializerMethodField()
    data_agendamento = serializers.SerializerMethodField()
    medico = DoctorSerializer(source="schedule.doctor")

    class Meta:
        model = Consult
        fields = ["id", "dia", "horario", "data_agendamento", "medico"]

    def get_dia(self, obj):
        return obj.schedule.day.strftime("%d/%m/%Y")

    def get_horario(self, obj):
        return obj.hour.strftime("%H:%M")

    def get_data_agendamento(self, obj):
        return obj.created_at.astimezone().strftime("%d/%m/%Y %H:%M")
