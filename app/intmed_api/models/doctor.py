from django.db import models

from .speciality import Speciality


class Doctor(models.Model):
    id: int = models.AutoField(primary_key=True)
    name: str = models.CharField(max_length=100, blank=False, null=False)
    crm: str = models.CharField(max_length=15, unique=True, blank=False, null=False)
    email: str = models.EmailField()
    speciality = models.ForeignKey(
        Speciality,
        on_delete=models.SET_NULL,
        related_name="specialities",
        null=True,
        blank=True,
        verbose_name="Especialidade",
    )

    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"

    def __str__(self) -> str:
        return f"{self.name} - {self.crm}"
