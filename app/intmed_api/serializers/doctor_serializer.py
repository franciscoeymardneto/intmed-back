from rest_framework import serializers

from ..models import Doctor, Speciality


class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = ["name"]


class DoctorSerializer(serializers.ModelSerializer):
    nome = serializers.SerializerMethodField()
    especialidade = serializers.SerializerMethodField()

    def get_nome(self, obj):
        return obj.name

    def get_especialidade(self, obj):
        speciality = SpecialitySerializer(obj.speciality).data.get("name")

        if speciality:
            return speciality
        else:
            return ""

    class Meta:
        model = Doctor
        fields = ["id", "crm", "nome", "email", "especialidade"]
