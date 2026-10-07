"""
Events app — CRUD + cancel endpoints.

Product requirements (read carefully):
- List events with optional `club` filter (exact club id).
- Create / update / delete events.
- POST cancel: set status to "cancelled" and persist it.
"""

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Event
from .serializers import EventSerializer


@api_view(["GET", "POST"])
def list_or_create_events(request):
    if request.method == "POST":
        return create_event(request)
    return list_events(request)


def list_events(request):
    qs = Event.objects.select_related("club").all()

    club = (request.GET.get("club") or "").strip()

    status = (request.GET.get("status") or "").strip().lower()
    if status:
        qs = qs.filter(status=status)

    return Response(EventSerializer(qs.order_by("event_date", "id"), many=True).data)


def create_event(request):
    serializer = EventSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    event = serializer.save()
    return Response(EventSerializer(event).data, status=201)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def event_detail(request, pk):
    event = get_object_or_404(Event.objects.select_related("club"), pk=pk)

    if request.method == "GET":
        return Response(EventSerializer(event).data)

    if request.method == "DELETE":
        event.delete()
        return Response(status=204)

    partial = request.method == "PATCH"
    serializer = EventSerializer(event, data=request.data, partial=partial)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    event = serializer.save()
    return Response(EventSerializer(event).data)


@api_view(["POST"])
def cancel_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.status = "cancelled"
    event.save()
    return Response(EventSerializer(event).data)
