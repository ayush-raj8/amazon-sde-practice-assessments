from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    club_name = serializers.CharField(source="club.name", read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "club",
            "club_name",
            "event_date",
            "location",
            "capacity",
            "status",
        ]
