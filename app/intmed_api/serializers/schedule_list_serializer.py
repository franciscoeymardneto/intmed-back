from rest_framework import serializers

from ..models import Schedule
from .doctor_serializer import DoctorSerializer


class ScheduleSerializer(serializers.ModelSerializer):
    medico = serializers.SerializerMethodField()
    dia = serializers.SerializerMethodField()
    horarios = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = ["id", "medico", "dia", "horarios"]

    def get_medico(self, obj):
        return DoctorSerializer(obj.doctor).data

    def get_dia(self, obj):
        return obj.day.strftime("%d/%m/%Y")

    def get_horarios(self, obj):
        return [hour.strftime("%H:%M") for hour in obj.hours]
