from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from .schedule import Schedule


class Consult(models.Model):
    id: int = models.AutoField(primary_key=True)
    schedule = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, related_name="schedule", null=False, verbose_name="Agenda"
    )
    hour: models.TimeField = models.TimeField(verbose_name="Horário")
    client = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_consult", null=True, blank=True, verbose_name="Cliente"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def NoScheduleConsultWithPastDayHour(self):
        current_day = timezone.localtime(timezone.now()).date()
        current_hour = timezone.localtime(timezone.now()).time()

        if self.schedule.day < current_day:
            raise ValidationError("Não é possível agendar uma consulta para um dia passado.")

        if (self.schedule.day == current_day) and (current_hour > self.hour):
            raise ValidationError("Não é possível agendar uma consulta para um horário passado.")

    def ValidateHourInSchedule(self):
        if self.hour not in self.schedule.hours:
            raise ValidationError("O horário da consulta não está disponível na agenda.")

    def RemoveAvailableHourFromSchedule(self):
        self.schedule.hours.remove(self.hour)
        self.schedule.save(update_fields=['hours'])

    def CanDeleteConsult(self):
        current_day = timezone.localtime(timezone.now()).date()
        current_hour = timezone.localtime(timezone.now()).time()

        if not (
            self.schedule.day > current_day or
            (
                self.schedule.day == current_day and self.hour > current_hour
            )
        ):
            raise ValidationError('Não é possível desmarcar uma consulta que estava marcada para um horário passado.')

    def ReturnHourToScheduleWhenDeleteConsult(self):
        self.schedule.hours.append(self.hour)
        self.schedule.hours.sort()
        self.schedule.save(update_fields=['hours'])

    def clean(self):
        self.ValidateHourInSchedule()
        self.NoScheduleConsultWithPastDayHour()

    class Meta:
        unique_together = ("schedule", "hour")
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"

    def save(self, *args, **kwargs):
        self.full_clean()
        self.RemoveAvailableHourFromSchedule()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.CanDeleteConsult()
        super().delete(*args, **kwargs)
        self.ReturnHourToScheduleWhenDeleteConsult()

    def __str__(self) -> str:
        return f"{self.schedule.__str__()} - {self.hour.strftime("%H:%M")}"
