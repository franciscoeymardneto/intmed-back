from django.urls import path

from .views import (consults_view, createUser, delete_consult, list_doctors,
                    list_schedules, list_speciality, login)

urlpatterns = [
    path("especialidades", list_speciality, name="speciality"),
    path("consultas", consults_view, name="consults_view"),
    path("consultas/<int:consulta_id>", delete_consult, name="consults_view"),
    path("medicos", list_doctors, name="list_doctors"),
    path("agendas", list_schedules, name="list_schedules"),
    path("users", createUser, name="register"),
    path("users/login", login, name="login"),
]
