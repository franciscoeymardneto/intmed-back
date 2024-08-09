from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import Doctor, Schedule
from ..serializers import ScheduleSerializer


@swagger_auto_schema(
    operation_description="Método para listar as agendas dos médicos com base em filtros de ID, CRM e intervalo de datas.",
    method="get",
    manual_parameters=[
        openapi.Parameter(
            "medico",
            openapi.IN_QUERY,
            description="ID do médico",
            type=openapi.TYPE_INTEGER,
            explode=True,
        ),
        openapi.Parameter(
            "crm",
            openapi.IN_QUERY,
            description="CRM do médico",
            type=openapi.TYPE_INTEGER,
            explode=True,
        ),
        openapi.Parameter(
            "data_inicio",
            openapi.IN_QUERY,
            description="Data de início do intervalo",
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_DATE,
        ),
        openapi.Parameter(
            "data_final",
            openapi.IN_QUERY,
            description="Data final do intervalo",
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_DATE,
        ),
    ],
)
@api_view(["GET"])
def list_schedules(request):
    now = timezone.localtime(timezone.now())
    today = now.date()
    filters = {}

    try:
        filters = define_filters(request, filters)
    except ValidationError as error:
        return Response(
            {"error": error.messages.pop()}, status=status.HTTP_400_BAD_REQUEST
        )

    queryset = Schedule.objects.filter(
        Q(day__gte=today),
        Q(hours__len__gt=0),
        **filters,
    ).order_by("day")

    serializer = ScheduleSerializer(remove_past_hours(queryset), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def remove_past_hours(queryset):
    now = timezone.localtime(timezone.now())
    today = now.date()
    current_time = now.time()
    new_object_list = []

    for obj in queryset:
        if obj.day == today:
            new_hours = [hour for hour in obj.hours if hour >= current_time]
            if new_hours:
                new_object = Schedule(
                    id=obj.id, day=obj.day, doctor=obj.doctor, hours=new_hours
                )
                new_object_list.append(new_object)
        else:
            new_object = Schedule(
                id=obj.id, day=obj.day, doctor=obj.doctor, hours=obj.hours
            )
            new_object_list.append(new_object)

    return new_object_list


def define_filters(request, filters):
    medico_ids = request.query_params.getlist("medico", [])
    crm_numbers = request.query_params.getlist("crm", [])
    data_inicio = request.query_params.get("data_inicio", None)
    data_final = request.query_params.get("data_final", None)

    if medico_ids:
        filters["doctor__id__in"] = medico_ids

    if crm_numbers:
        doctors = Doctor.objects.filter(crm__in=crm_numbers)
        filters["doctor__in"] = doctors

    if data_inicio and data_final:
        try:
            start_date = timezone.datetime.strptime(data_inicio, "%Y-%m-%d").date()
            end_date = timezone.datetime.strptime(data_final, "%Y-%m-%d").date()
            if start_date > end_date:
                raise ValidationError(
                    "Data de início deve ser anterior ou igual a Data final.",
                    code="invalid_date",
                )
            filters["day__range"] = [start_date, end_date]
        except ValueError:
            raise ValidationError(
                "Formato de data inválido.", code="invalid_date_format"
            )

    return filters
