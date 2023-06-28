from datetime import datetime
import pytz
from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', required=False)

    class Meta:
        model = Event
        fields = ['pk', 'name', 'start_date', 'end_date', 'description', 'capacity', 'attendees', 'created_by',
                  'created', 'updated']

    def validate(self, data):
        if data['start_date'] < datetime.now().replace(tzinfo=pytz.utc):
            raise serializers.ValidationError("Event can't start in the past.")

        if data['end_date'] < datetime.now().replace(tzinfo=pytz.utc):
            raise serializers.ValidationError("Event can't end in the past.")

        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("Event can't end before it starts.")

        return data
