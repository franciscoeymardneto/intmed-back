from django.db import models


class Speciality(models.Model):
    id: int = models.AutoField(primary_key=True)
    name: str = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = "Especialidade"
        verbose_name_plural = "Especialidades"

    def __str__(self) -> str:
        return f"{self.name}"
