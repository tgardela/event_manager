from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Event
from .serializers import EventSerializer


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['GET', 'POST', 'head', 'patch', 'PUT', 'DELETE']

    # filles 'created_by' field with the user that creates the object
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #
    #     if instance.created_by != request.user:
    #         return self.http_method_not_allowed(request, *args, **kwargs)
    #
    #     return super().update(request, *args, **kwargs)

    # def get_permissions(self):
    #     if self.action == 'update':
    #         # Check if the requesting user is the creator of the object
    #         instance = self.get_object()
    #         if instance.created_by != self.request.user:
    #             self.permission_classes = []
    #
    #     return super().get_permissions()

    # def partial_update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #
    #     # Check if the requesting user is the creator of the object
    #     if instance.created_by != request.user:
    #         return self.http_method_not_allowed(request, *args, **kwargs)
    #
    #     return super().partial_update(request, *args, **kwargs)