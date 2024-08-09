from rest_framework import serializers

from ..models import Speciality


class SpecialitySerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source="name")

    class Meta:
        model = Speciality
        fields = ["id", "nome"]
