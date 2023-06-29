from datetime import (
    datetime,
    timedelta,
    )
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import pytz
from rest_framework import status
from rest_framework.test import (
    APIClient,
    APIRequestFactory,
    APITestCase,
    force_authenticate,
    )

from events.models import Event
from events.views import EventViewSet


class EventViewSetTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username='testuser')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.event = Event.objects.create(
            name='Test Event',
            start_date=datetime.utcnow().replace(tzinfo=pytz.utc),
            end_date=(datetime.utcnow().replace(tzinfo=pytz.utc) + timedelta(hours=2)).isoformat(),
            capacity=100,
            created_by=self.user
        )
        self.url = f'/events/{self.event.pk}/'
        self.viewset = EventViewSet

    def test_retrieve_event(self):
        response = self.client.get(f'/events/{self.event.pk}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test Event')

    def test_create_event(self):
        data = {
            'name': 'New Event',
            'start_date': (datetime.now() + timedelta(days=2)).isoformat(),
            'end_date': (datetime.now() + timedelta(days=3)).isoformat(),
            'capacity': 50
        }
        response = self.client.post('/events/', data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'New Event')
        self.assertEqual(response.data['created_by'], self.user.username)

    def test_update_event(self):
        start_date = (datetime.now() + timedelta(days=2)).replace(microsecond=0).isoformat() + 'Z'
        end_date = (datetime.now() + timedelta(days=3)).replace(microsecond=0).isoformat() + 'Z'

        data = {
            'name': 'Updated Event',
            'start_date': start_date,
            'end_date': end_date,
            'capacity': 75
            }
        response = self.client.put(f'/events/{self.event.pk}/', data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Updated Event')
        self.assertEqual(response.data['start_date'], start_date)
        self.assertEqual(response.data['end_date'], end_date)
        self.assertEqual(response.data['capacity'], 75)

    def test_update_event_permission_denied(self):
        another_user = User.objects.create(username='anotheruser')
        client = APIClient()
        client.force_authenticate(user=another_user)
        data = {
            'name': 'Updated Event',
            'start_date': '2023-03-01',
            'end_date': '2023-03-02',
            'capacity': 75
        }
        response = client.put(f'/events/{self.event.pk}/', data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'To update an event, you must be the creator of that event.')

    def test_register_endpoint(self):
        self.request = self.factory.post(f'{self.url}register/')
        force_authenticate(self.request, user=self.user)

        response = self.viewset.as_view({'post': 'register'})(self.request, pk=self.event.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['event_id'], self.event.pk)
        self.assertEqual(response.data['user_id'], self.user.id)
        self.assertIn('message', response.data)

        if self.event.attendees.count() == self.event.capacity:
            self.assertEqual(response.data['message'], 'The attendance list for this event is full. You cannot register at this time.')  # noqa

        elif self.event.start_date < datetime.utcnow().replace(tzinfo=pytz.utc):
            self.assertEqual(response.data['message'], 'The event has already started, you cannot register to it.')

        else:
            self.event.refresh_from_db()
            self.assertEqual(response.data['message'], f'Registered user: {self.user.id} for event: {self.event.pk}')
            self.assertIn(self.user, self.event.attendees.all())

    def test_register_endpoint_full_attendance(self):
        self.event.capacity = 0
        self.event.save()

        self.request = self.factory.post(f'{self.url}register/')
        force_authenticate(self.request, user=self.user)
        response = self.viewset.as_view({'post': 'register'})(self.request, pk=self.event.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['event_id'], self.event.pk)
        self.assertEqual(response.data['user_id'], self.user.id)
        self.assertEqual(response.data['message'], 'The attendance list for this event is full. You cannot register at this time.')  # noqa
        self.event.refresh_from_db()
        self.assertNotIn(self.user, self.event.attendees.all())

    def test_register_endpoint_event_started(self):
        self.event.start_date = datetime.utcnow().replace(tzinfo=pytz.utc)
        self.event.save()

        self.request = self.factory.post(f'{self.url}register/')
        force_authenticate(self.request, user=self.user)

        response = self.viewset.as_view({'post': 'register'})(self.request, pk=self.event.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['event_id'], self.event.pk)
        self.assertEqual(response.data['user_id'], self.user.id)
        self.assertEqual(response.data['message'], 'The event has already started, you cannot register to it.')

    def test_unregister_endpoint(self):
        self.event.attendees.add(self.user)
        self.event.save()

        self.request = self.factory.post(f'{self.url}unregister/')
        force_authenticate(self.request, user=self.user)

        response = self.viewset.as_view({'post': 'unregister'})(self.request, pk=self.event.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['event_id'], self.event.pk)
        self.assertEqual(response.data['user_id'], self.user.id)
        self.assertEqual(response.data['message'], f'Unregistered user: {self.user.id} for event: {self.event.pk}')
        self.event.refresh_from_db()
        self.assertNotIn(self.user, self.event.attendees.all())

    def test_filter_by_date(self):
        Event.objects.create(
            name='Event 1',
            start_date=datetime.strptime('2023-03-05', '%Y-%m-%d').replace(tzinfo=pytz.utc),
            end_date=datetime.strptime('2023-03-05', '%Y-%m-%d').replace(tzinfo=pytz.utc),
            capacity=10,
            created_by=self.user
            )
        Event.objects.create(
            name='Event 2',
            start_date=datetime.strptime('2023-03-02', '%Y-%m-%d').replace(tzinfo=pytz.utc),
            end_date=datetime.strptime('2023-03-02', '%Y-%m-%d').replace(tzinfo=pytz.utc),
            capacity=10,
            created_by=self.user
            )
        response = self.client.get(reverse('Events-list'), {'date': '2023-03-05'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Event 1')

    def test_filter_past_events(self):
        Event.objects.create(
            name='Event 1',
            start_date=datetime.strptime('2023-03-05', '%Y-%m-%d').replace(tzinfo=pytz.utc),
            end_date=datetime.strptime('2023-03-06', '%Y-%m-%d').replace(tzinfo=pytz.utc),
            capacity=10,
            created_by=self.user
            )
        Event.objects.create(
            name='Event 2',
            start_date=(datetime.utcnow().replace(tzinfo=pytz.utc) + timezone.timedelta(days=1)).isoformat(),
            end_date=(datetime.utcnow().replace(tzinfo=pytz.utc) + timezone.timedelta(days=1, hours=1)).isoformat(),
            capacity=10,
            created_by=self.user
            )

        response = self.client.get(reverse('Events-list'), {'past': 'true'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'Test Event')
        self.assertEqual(response.data[1]['name'], 'Event 1')

    def test_filter_future_events(self):
        Event.objects.create(
            name='Event 1',
            start_date=datetime.utcnow().replace(tzinfo=pytz.utc).isoformat(),
            end_date=(datetime.utcnow().replace(tzinfo=pytz.utc) + timezone.timedelta(hours=1)).isoformat(),
            capacity=10,
            created_by=self.user
            )
        Event.objects.create(
            name='Event 2',
            start_date=(datetime.utcnow().replace(tzinfo=pytz.utc) + timezone.timedelta(days=1)).isoformat(),
            end_date=(datetime.utcnow().replace(tzinfo=pytz.utc) + timezone.timedelta(days=1, hours=1)).isoformat(),
            capacity=10,
            created_by=self.user
            )
        Event.objects.create(
            name='Event 3',
            start_date=(datetime.utcnow().replace(tzinfo=pytz.utc) - timezone.timedelta(days=2)).isoformat(),
            end_date=(datetime.utcnow().replace(tzinfo=pytz.utc) + timezone.timedelta(days=2, hours=1)).isoformat(),
            capacity=10,
            created_by=self.user
            )

        response = self.client.get(reverse('Events-list'), {'future': 'true'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Event 2')
