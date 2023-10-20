from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from heritagehub.heritagehubapp.models import EventModel
from rest_framework import status

class EventViewSetTests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='adminTest', password='azerty1234', email='adminTest@test.com')
        self.client.force_authenticate(user=self.user)
        self.event_data={
            "event_name":"anniv de mamadou",
            "person_id":1,
            "event_type":"annivairsaire"
        }
        self.test_event = EventModel.objects.create(created_by=self.user.id,**self.event_data)

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
        response = self.client.post('/events/', self.event_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(EventModel.objects.count(),2)
        self.assertEquals(EventModel.objects.last().created_by,self.user.id)  

    def test_retreive_event(self):
        """
        Test that an authenticated user can retrieve a event and that the 'created_by' field matches the user's ID.
        """
        response = self.client.get(f'/events/{self.test_event.id}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['created_by'], self.user.id)
    
    def test_partial_update_event_authenticate_user(self):
        """
        Test that an authenticated user can partially update a event, and 'created_by' field is updated.
        """
        updated_data = {'created_by':2}
        response = self.client.patch(f'/events/{self.test_event.id}/',updated_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.test_event.refresh_from_db()
        self.assertEquals(self.test_event.created_by, 2)

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