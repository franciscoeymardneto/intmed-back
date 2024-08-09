from django.core.exceptions import ValidationError
from django.test import TestCase

from ...models import Doctor, Speciality


class DoctorModelTestSuit(TestCase):
    def setUp(self):
        self.speciality = Speciality.objects.create(name="Cardiologia")

    def test_create_doctor(self):
        # Testa a criação de um médico com todos os campos válidos
        doctor = Doctor.objects.create(
            name="Dr. Edward Richtofen",
            crm="12345678-9/CE",
            email="dr.ed.richtofen@intmed.com",
            speciality=self.speciality,
        )
        self.assertEqual(doctor.name, "Dr. Edward Richtofen")
        self.assertEqual(doctor.crm, "12345678-9/CE")
        self.assertEqual(doctor.email, "dr.ed.richtofen@intmed.com")
        self.assertEqual(doctor.speciality, self.speciality)

    def test_str_method(self):
        # Testa o método __str__ do modelo
        doctor = Doctor.objects.create(
            name="Dr. Ludwig Maxis",
            crm="98765432-1/CE",
            email="dr.lud.maxis@intmed.com",
            speciality=self.speciality,
        )
        self.assertEqual(str(doctor), "Dr. Ludwig Maxis - 98765432-1/CE")

    def test_unique_crm(self):
        # Testa o unique do campo crm
        Doctor.objects.create(
            name="Dr. Stephen Strange",
            crm="12345678-9/CE",
            email="dr.stephen.strange@intmed.com",
            speciality=self.speciality,
        )
        with self.assertRaises(ValidationError):
            doctor = Doctor(
                name="Dra. Maria Oliveira",
                crm="12345678-9/CE",
                email="dr.maria.oliveira@intmed.com",
                speciality=self.speciality,
            )
            doctor.full_clean()

    def test_optional_speciality(self):
        # Testa que o campo speciality é opcional
        doctor = Doctor.objects.create(
            name="Dr. Jane Doe",
            crm="87654321-0/SP",
            email="dr.jane.doe@intmed.com",
        )
        self.assertIsNone(doctor.speciality)

    def test_set_null_when_speciality_was_deleted(self):
        # Testa que o campo speciality é setado null quando
        # a especialidade é excluida
        speciality = Speciality.objects.create(name="Neurologista")
        doctor = Doctor.objects.create(
            name="Dr. Emily Carter",
            crm="23456789-1/RJ",
            email="dr.emily.carter@intmed.com",
            speciality=speciality,
        )
        self.assertEqual(doctor.speciality.name, "Neurologista")

        speciality.delete()
        doctor = Doctor.objects.get(id=doctor.id)

        self.assertIsNone(doctor.speciality)

    def test_blank_name_not_allowed(self):
        # Testa que o campo nome não pode ser em branco
        with self.assertRaises(ValidationError):
            doctor = Doctor(
                name="",
                crm="01234567-9/GO",
                email="dr.ava.thomas@intmed.com",
                speciality=self.speciality,
            )
            doctor.full_clean()

    def test_blank_crm_not_allowed(self):
        # Testa que o campo crm não pode ser em branco
        with self.assertRaises(ValidationError):
            doctor = Doctor(
                name="Dr. Lucas Anderson",
                crm="",
                email="dr.lucas.anderson@intmed.com",
                speciality=self.speciality,
            )
            doctor.full_clean()
