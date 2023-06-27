import datetime
from django.db import models
from rest_framework.exceptions import ValidationError


class Event(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)
    capacity = models.IntegerField(null=False)
    attendees = models.ManyToManyField('auth.User', related_name='attendees', blank=True)
    created_by = models.ForeignKey(to='auth.User', on_delete=models.DO_NOTHING, related_name='created_events')

    def __str__(self):
        return self.name

    def get_attendees(self):
        return "\n".join([a.username for a in self.attendees.all()])

    def save(self, *args, **kwargs):
        if self.end_date < self.start_date:
            raise ValidationError("The end date cannot be in the past!")

        # if self.start_date < datetime.datetime.today() or self.end_date < datetime.datetime.today():
        #     raise ValidationError("The end date cannot be in the past!")

        super(Event, self).save(*args, **kwargs)
