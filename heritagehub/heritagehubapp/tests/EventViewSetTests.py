from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from heritagehub.heritagehubapp.models import EventModel
from heritagehub.heritagehubapp.models import PersonModel
from rest_framework import status


class EventViewSetTests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='adminTest', password='azerty1234', email='adminTest@test.com')
        self.user2 = User.objects.create_user(
            username='adminTest2', password='azerty1234', email='adminTest2@test.com')
        self.client.force_authenticate(user=self.user)

        person_data = {
            "first_name": "ibrahim",
            "last_name": "sarr",
            "birth_date": "2000-08-07",
            "familly_id": None,
            "child_from_marriage": None
        }

        self.test_person = PersonModel.objects.create(
            created_by=self.user, **person_data)

        self.event_data = {
            "event_name": "test event name",
            "person_id": self.test_person,
            "event_type": "annivairsaire"
        }

        self.test_event = EventModel.objects.create(
            created_by=self.user, **self.event_data)

    def test_list_events(self):
        """
        Test that the API endpoint for listing events returns a 200 status code and non-empty data.
        """
        response = self.client.get('/events/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_create_event_authenticate_user(self):
        """
        Test that an authenticated user can create a new event.
        """

        event_data = {
            "event_name": "test event name",
            "person_id": 1,
            "event_type": "annivairsaire"
        }
        response = self.client.post('/events/', event_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(EventModel.objects.count(), 2)
        self.assertEquals(EventModel.objects.last().created_by, self.user)
        self.assertEquals(
            EventModel.objects.last().event_name, "test event name")

    def test_retreive_event(self):
        """
        Test that an authenticated user can retrieve a event and that the 'created_by' field matches the user's ID.
        """
        response = self.client.get(f'/events/{self.test_event.id}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['created_by'], self.user.id)
        self.assertEquals(response.data['event_name'], "test event name")

    def test_partial_update_event_authenticate_user(self):
        """
        Test that an authenticated user can partially update a event, and 'created_by' field is updated.
        """
        updated_data = {'created_by': self.user2.id,
                        'event_name': 'event name updated'}
        response = self.client.patch(
            f'/events/{self.test_event.id}/', updated_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.test_event.refresh_from_db()
        self.assertEquals(self.test_event.created_by, self.user2)
        self.assertEquals(self.test_event.event_name, 'event name updated')

    def test_destroy_event_authenticated_user(self):
        """
        Test that an authenticated user can delete a event and it no longer exists in the database.
        """
        response = self.client.delete(f'/events/{self.test_event.id}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        with self.assertRaises(EventModel.DoesNotExist):
            EventModel.objects.get(id=self.test_event.id)

    def test_destroy_event_noexistant(self):
        """
        Test that attempting to delete a non-existent event returns a 404 Not Found status.
        """
        response = self.client.delete('/events/999/')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
