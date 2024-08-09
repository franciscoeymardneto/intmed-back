from rest_framework import serializers


class CreateScheduleSerializer(serializers.Serializer):
    agenda_id = serializers.IntegerField()
    cliente_id = serializers.IntegerField()
    horario = serializers.TimeField()
