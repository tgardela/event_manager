from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
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
