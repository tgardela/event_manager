from datetime import datetime
import pytz
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Event
from .serializers import EventSerializer


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]

    # filles 'created_by' field with the user that creates the object
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    # checks if the user updating the event is its creator
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.created_by != request.user:
            message = 'To update an event, you must be the creator of that event.'
            raise PermissionDenied(message)

        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        event = self.get_object()

        if event.attendees.count() == event.capacity:
            message = 'The attendance list for this event is full. You cannot register at this time.'
        elif event.start_date < datetime.now().replace(tzinfo=pytz.utc):
            message = 'The event has already started, you cannot register to it.'
        else:
            event.attendees.add(request.user)
            event.save()
            message = f'Registered user: {request.user.id} for event: {event.pk}'

        response_data = {
            'message': message,
            'event_id': event.pk,
            'user_id': request.user.id,
            }

        return Response(response_data)

    @action(detail=True, methods=['post'])
    def unregister(self, request, pk=None):
        event = self.get_object()

        event.attendees.remove(request.user)
        event.save()

        response_data = {
            'message': f'Unregistered user: {request.user.id} for event: {event.pk}',
            'event_id': event.pk,
            'user_id': request.user.id,
            }

        return Response(response_data)
