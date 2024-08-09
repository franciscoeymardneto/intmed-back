from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from ...models import Consult, Doctor, Schedule, Speciality


class CosultModelTestSuit(TestCase):
    currentTimezone = timezone.localtime(timezone.now())
    hours = [
        (currentTimezone + timedelta(minutes=1)).time()
    ]

    def setUp(self):
        self.speciality = Speciality.objects.create(name="Cardiologia")

        self.doctor = Doctor.objects.create(
            name="Dr. Edward Richtofen",
            crm="12345678-9/CE",
            email="dr.ed.richtofen@intmed.com",
            speciality=self.speciality,
        )

        self.schedule = Schedule.objects.create(
            doctor=self.doctor, day=self.currentTimezone.date(), hours=self.hours
        )

        self.client = User.objects.create_user(
            username="client", password="clientpassword", email="client@example.com"
        )

    def test_create_consult(self):
        # Testa a criação de uma consulta com dados válidos
        hour = (self.currentTimezone + timedelta(minutes=1)).time()
        consult = Consult.objects.create(
            schedule=self.schedule, hour=hour, client=self.client
        )
        self.assertEqual(consult.schedule, self.schedule)
        self.assertEqual(consult.hour, hour)
        self.assertEqual(consult.client, self.client)

    def test_str_method(self):
        # Testa o método __str__ do modelo

        time = (self.currentTimezone + timedelta(minutes=1)).time()
        schedule = Schedule.objects.create(
            doctor=self.doctor,
            day=(self.currentTimezone + timedelta(days=1)).date(),
            hours=[time]
        )

        consult = Consult.objects.create(
            schedule=schedule, hour=time, client=self.client
        )
        self.assertEqual(
            str(consult),
            f"{schedule.__str__()} - {consult.hour.strftime("%H:%M")}"
        )

    def test_no_schedule_consult_with_past_day(self):
        # Testa a validação de não poder marcar consulta para um dia passado
        currentTimezone = (self.currentTimezone - timedelta(days=1))

        past_schedule = Schedule(
            doctor=self.doctor,
            day=currentTimezone.date(),
            hours=[currentTimezone.time()]
        )
        with self.assertRaisesMessage(ValidationError,"Não é possível agendar uma consulta para um dia passado."):
            consult = Consult(
                schedule=past_schedule,
                hour=currentTimezone.time(),
                client=self.client
            )
            consult.full_clean()

    def test_no_schedule_consult_with_past_hour(self):
        # Testa a validação de não poder marcar consulta para um horário passado
        currentTimezone = (self.currentTimezone - timedelta(hours=1))

        past_schedule = Schedule(
            doctor=self.doctor,
            day=currentTimezone.date(),
            hours=[currentTimezone.time()]
        )
        with self.assertRaisesMessage(ValidationError,"Não é possível agendar uma consulta para um horário passado."):
            consult = Consult(
                schedule=past_schedule,
                hour=currentTimezone.time(),
                client=self.client
            )
            consult.full_clean()

    def test_no_schedule_consult_with_no_hour_available(self):
        # Testa a validação de não poder marcar consulta para um horário não
        # disponivel na agenda
        noAvailableHour = (self.currentTimezone + timedelta(hours=1)).time()

        past_schedule = Schedule(
            doctor=self.doctor,
            day=self.currentTimezone.date(),
            hours=[self.currentTimezone.time()]
        )
        with self.assertRaisesMessage(ValidationError,"O horário da consulta não está disponível na agenda."):
            consult = Consult(
                schedule=past_schedule,
                hour=noAvailableHour,
                client=self.client
            )
            consult.full_clean()

    def test_remove_available_hour_from_schedule(self):
        # Testa se a hora da consulta é removida da agenda ao salvar a consulta
        time = (self.currentTimezone + timedelta(minutes=1)).time()
        schedule = Schedule.objects.create(
            doctor=self.doctor,
            day=(self.currentTimezone + timedelta(days=1)).date(),
            hours=[time]
        )
        Consult.objects.create(
            schedule=schedule,
            hour=time,
            client=self.client
        )

        schedule.refresh_from_db()
        self.assertNotIn(time, schedule.hours)

    def test_return_hour_to_schedule_when_delete_consult(self):
        # Testa se a hora da consulta é retornada à agenda ao deletar a consulta
        time = (self.currentTimezone + timedelta(minutes=1)).time()
        schedule = Schedule.objects.create(
            doctor=self.doctor,
            day=(self.currentTimezone + timedelta(days=1)).date(),
            hours=[time]
        )

        consult = Consult.objects.create(
            schedule=schedule,
            hour=time,
            client=self.client
        )
        consult.delete()
        schedule.refresh_from_db()
        self.assertIn(time, schedule.hours)

    def test_no_delete_consult_with_past_hour(self):
        # Testa a validação de não poder desmarcar uma consulta de um horário passado
        currentTimezone = (self.currentTimezone - timedelta(hours=1))

        past_schedule = Schedule(
            doctor=self.doctor,
            day=currentTimezone.date(),
            hours=[currentTimezone.time()]
        )
        with self.assertRaisesMessage(ValidationError,"'Não é possível desmarcar uma consulta que estava marcada para um horário passado"):
            consult = Consult(
                schedule=past_schedule,
                hour=currentTimezone.time(),
                client=self.client
            )
            consult.CanDeleteConsult()

    def test_clean_method(self):
        # Testa o método clean para garantir que as validações estão sendo aplicadas
        hour = (self.currentTimezone + timedelta(days=1)).time()
        schedule = Schedule.objects.create(
            doctor=self.doctor,
            day=(self.currentTimezone + timedelta(days=1)).date(),
            hours=[hour]
        )

        consult = Consult(
            schedule=schedule, hour=hour, client=self.client
        )
        try:
            consult.clean()  # Deve passar sem exceções
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly!")