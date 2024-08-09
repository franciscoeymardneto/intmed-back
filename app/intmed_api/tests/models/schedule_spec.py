from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from ...models import Doctor, Schedule, Speciality


class ScheduleModelTestSuit(TestCase):
    currentTimezone = timezone.localtime(timezone.now())
    hours = [
        (currentTimezone + timedelta(minutes=1)).time()
    ]

    def setUp(self):
        self.doctor = Doctor.objects.create(
            name="Dr. Edward Richtofen",
            crm="12345678-9/CE",
            email="dr.ed.richtofen@intmed.com",
        )
        self.doctor.speciality = Speciality.objects.create(name="Cardiologia")

    def test_create_schedule(self):
        # Testa a criação de uma agenda com todos os campos válidos
        schedule = Schedule.objects.create(
            doctor=self.doctor, day=self.currentTimezone.date(), hours=self.hours
        )

        self.assertEqual(schedule.doctor, self.doctor)
        self.assertEqual(schedule.day, self.currentTimezone.date())
        self.assertEqual(schedule.hours, self.hours)

    def test_str_method(self):
        # Testa o método __str__ do modelo
        schedule = Schedule.objects.create(
            doctor=self.doctor, day=self.currentTimezone.date(), hours=self.hours
        )
        self.assertEqual(
            str(schedule),
            f"Dr. Edward Richtofen - {self.currentTimezone.date().strftime("%d/%m/%Y")}"
        )

    def test_list_consult_from_this_schedule(self):
        # Testa o método ListConsultFromThisSchedule
        consult_time = (self.currentTimezone + timedelta(minutes=1)).time()
        schedule = Schedule.objects.create(
            doctor=self.doctor, day=self.currentTimezone.date(), hours=self.hours
        )
        from ...models import Consult
        Consult.objects.create(schedule=schedule, hour=consult_time)
        self.assertIn(consult_time, schedule.ListConsultFromThisSchedule())

    def test_no_save_schedule_with_past_date(self):
        # Testa a validação de não poder criar uma agenda com uma data passada

        with self.assertRaisesMessage(
            ValidationError,
            "Não é possível criar uma agenda para um dia passado."
        ):
            schedule = Schedule.objects.create(
                doctor=self.doctor,
                day=(self.currentTimezone - timedelta(days=1)).date(),
                hours=self.hours
            )
            schedule.full_clean()

    def test_no_save_schedule_with_past_hour(self):
        # Testa a validação de não poder criar uma agenda para hoje com
        # um horário passado
        hour = (self.currentTimezone - timedelta(hours=1)).time()
        with self.assertRaisesMessage(
            ValidationError,
            f"Horário passado: {hour}. Não é possível adicionar horários que já passaram."
        ):
            schedule = Schedule.objects.create(
                doctor=self.doctor,
                day=self.currentTimezone.date(),
                hours=[hour]
            )
            schedule.full_clean()

    def test_no_save_schedule_with_duplicate_hours(self):
        # Testa a validação de não poder criar uma agenda com horários duplicados
        hour = (self.currentTimezone + timedelta(minutes=1)).time()
        with self.assertRaisesMessage(
            ValidationError,
            f"Horário duplicado: {hour}. Não é possível adicionar horários iguais."
        ):
            schedule = Schedule.objects.create(
                doctor=self.doctor,
                day=self.currentTimezone.date(),
                hours=[hour, hour]
            )
            schedule.full_clean()

    def test_no_save_schedule_with_allocated_hours(self):
        # Testa a validação de não poder adicionar à agenda um horário já marcado
        hour = (self.currentTimezone + timedelta(minutes=1)).time()

        schedule = Schedule.objects.create(
            doctor=self.doctor,
            day=self.currentTimezone.date(),
            hours=[hour]
        )

        from ...models import Consult
        Consult.objects.create(schedule=schedule, hour=hour)

        with self.assertRaisesMessage(
            ValidationError,
            f"Horário já alocado: {hour}. Não é possível adicionar horários que já estão " +
            "alocados nas consultas."
        ):
            schedule.hours.append(hour)
            schedule.save(updupdate_fields=['hours'])

    def test_clean_method(self):
        # Testa o método clean para garantir que as validações estão sendo aplicadas
        schedule = Schedule(
            doctor=self.doctor,
            day=self.currentTimezone.date(),
            hours=self.hours
        )
        try:
            schedule.clean()  # Deve passar sem exceções
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly!")