from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from ..models import Consult
from ..serializers import ConsultSerializer


def list_consults(request):
    client_id = request.query_params.get("clientId", None)

    now = timezone.localtime(timezone.now())
    today = now.date()
    current_time = now.time()

    if client_id is not None:
        queryset = Consult.objects.filter(
            Q(schedule__day__gt=today) | (Q(schedule__day=today) & Q(hour__gte=current_time)),
            client__id=client_id,
        ).order_by("schedule__day", "hour")
    else:
        queryset = Consult.objects.filter(
            Q(schedule__day__gt=today) | (Q(schedule__day=today) & Q(hour__gte=current_time)),
        ).order_by("schedule__day", "hour")


        print(f"LALALALALAL {queryset.count()} {today.strftime("%d/%m/%Y")} {current_time.strftime("%H/%M")} {client_id is not None}")

    serializer = ConsultSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
