from datetime import date

from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from .doctor import Doctor


class Schedule(models.Model):
    id: int = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="schedules",
        null=False,
        verbose_name="Médico"
    )
    day: date = models.DateField(verbose_name="Dia")
    hours = ArrayField(models.TimeField(), verbose_name="Horários Disponíveis", default=list, blank=True)

    class Meta:
        unique_together = ("doctor", "day")
        verbose_name = "Agenda"
        verbose_name_plural = "Agendas"

    def ListConsultFromThisSchedule(self) -> set[str]:
        # Importação tardia para evitar importação circular
        from .consult import Consult

        return set(Consult.objects.filter(schedule=self.id).values_list('hour', flat=True))

    def NoSaveScheduleWithPassDate(self):
        if self.day < timezone.localtime(timezone.now()).date():
            raise ValidationError(
                "Não é possível criar uma agenda para um dia passado.",
                code="invalid_day"
            )

    def NoSaveScheduleHoursWithPassHours(self):
        current_time = timezone.localtime(timezone.now()).time()
        current_day = timezone.localtime(timezone.now()).date()
        unique_hours = set()
        allocated_hours = self.ListConsultFromThisSchedule()

        for hour in self.hours:
            if hour in unique_hours:
                raise ValidationError(
                    f"Horário duplicado: {hour}. Não é possível adicionar horários iguais.",
                    code="duplicate_hour"
                )
            if self.day == current_day and hour <= current_time:
                raise ValidationError(
                    f"Horário passado: {hour}. Não é possível adicionar horários que já passaram.",
                    code="past_hour"
                )
            if hour in allocated_hours:
                raise ValidationError(
                    f"Horário já alocado: {hour}. Não é possível adicionar horários que já estão " +
                    "alocados nas consultas.",
                    code="allocated_hour"
                )
            unique_hours.add(hour)

    def clean(self):
        self.NoSaveScheduleWithPassDate()
        self.NoSaveScheduleHoursWithPassHours()

    def save(self, *args, **kwargs):
        self.full_clean()
        self.hours.sort()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.doctor.name} - {self.day.strftime("%d/%m/%Y")}"
