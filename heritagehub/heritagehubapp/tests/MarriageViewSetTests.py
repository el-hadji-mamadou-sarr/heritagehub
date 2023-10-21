from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from heritagehub.heritagehubapp.models import PersonModel
from heritagehub.heritagehubapp.models import MarriageModel
from rest_framework import status


class MarriageViewSetTests(APITestCase):

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

        self.marriage_data = {
            "husband_id": 1,
            "wife_id": 5,
            "marriage_date": "2023-08-07"
        }

        self.test_marriage = MarriageModel.objects.create(
            created_by=self.user, **self.marriage_data)

    def test_list_marriages(self):
        """
        Test that the API endpoint for listing marriages returns a 200 status code and non-empty data.
        """
        response = self.client.get('/marriages/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_create_marriage_authenticate_user(self):
        """
        Test that an authenticated user can create a new event.
        """

        response = self.client.post(
            '/marriages/', self.marriage_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(MarriageModel.objects.count(), 2)
        self.assertEquals(MarriageModel.objects.last().created_by, self.user)
        self.assertEquals(MarriageModel.objects.last().husband_id, 1)
        self.assertEquals(MarriageModel.objects.last().wife_id, 5)

    def test_retreive_marriage(self):
        """
        Test that an authenticated user can retrieve a event and that the 'created_by' field matches the user's ID.
        """
        response = self.client.get(f'/marriages/{self.test_marriage.id}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['created_by'], self.user.id)
        self.assertEquals(response.data['husband_id'], 1)
        self.assertEquals(response.data['wife_id'], 5)

    def test_partial_update_event_authenticate_user(self):
        """
        Test that an authenticated user can partially update a event, and 'created_by' field is updated.
        """
        updated_data = {'created_by': self.user2.id,
                        'husband_id': 2}
        response = self.client.patch(
            f'/marriages/{self.test_marriage.id}/', updated_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.test_marriage.refresh_from_db()
        self.assertEquals(self.test_marriage.created_by, self.user2)
        self.assertEquals(self.test_marriage.husband_id, 2)

    def test_destroy_event_authenticated_user(self):
        """
        Test that an authenticated user can delete a event and it no longer exists in the database.
        """
        response = self.client.delete(f'/marriages/{self.test_marriage.id}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        with self.assertRaises(MarriageModel.DoesNotExist):
            MarriageModel.objects.get(id=self.test_marriage.id)

    def test_destroy_event_noexistant(self):
        """
        Test that attempting to delete a non-existent event returns a 404 Not Found status.
        """
        response = self.client.delete('/marriages/999/')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
