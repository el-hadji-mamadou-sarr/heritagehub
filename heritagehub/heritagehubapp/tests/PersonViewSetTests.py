from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from heritagehub.heritagehubapp.models import PersonModel
from rest_framework import status


class PersonViewSetTests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='adminTest', password='azerty1234', email='adminTest@test.com')
        self.user2 = User.objects.create_user(
            username='adminTest2', password='azerty1234', email='adminTest2@test.com')
        self.client.force_authenticate(user=self.user)
        self.person_data = {
            "first_name": "test first_name",
            "last_name": "test last_name",
            "birth_date": "2000-08-07",
            "familly_id": None,
            "child_from_marriage": None
        }
        self.test_person = PersonModel.objects.create(
            created_by=self.user, **self.person_data)

    def test_list_persons(self):
        """
        Test that the API endpoint for listing persons returns a 200 status code and non-empty data.
        """
        response = self.client.get('/persons/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_create_person_authenticate_user(self):
        """
        Test that an authenticated user can create a new person.
        """
        response = self.client.post(
            '/persons/', self.person_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(PersonModel.objects.count(), 2)
        self.assertEquals(PersonModel.objects.last().created_by, self.user)

    def test_retreive_person(self):
        """
        Test that an authenticated user can retrieve a person.
        """
        response = self.client.get(f'/persons/{self.test_person.id}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['created_by'], self.user.id)
        self.assertEquals(
            response.data['first_name'], self.person_data['first_name'])
        self.assertEquals(
            response.data['last_name'], self.person_data['last_name'])

    def test_partial_update_person_authenticate_user(self):
        """
        Test that an authenticated user can partially update a person, and 'created_by',first_name and lat_name field are updated.
        """
        updated_data = {'created_by': self.user2.id,
                        "first_name": "test update first_name", "last_name": "test update last_name"}
        response = self.client.patch(
            f'/persons/{self.test_person.id}/', updated_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.test_person.refresh_from_db()
        self.assertEquals(self.test_person.created_by.id,
                          updated_data['created_by'])
        self.assertEquals(self.test_person.first_name,
                          updated_data['first_name'])
        self.assertEquals(self.test_person.last_name,
                          updated_data['last_name'])

    def test_destroy_person_authenticated_user(self):
        """
        Test that an authenticated user can delete a person and it no longer exists in the database.
        """
        response = self.client.delete(f'/persons/{self.test_person.id}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        with self.assertRaises(PersonModel.DoesNotExist):
            PersonModel.objects.get(id=self.test_person.id)

    def test_destroy_person_noexistant(self):
        """
        Test that attempting to delete a non-existent person returns a 404 Not Found status.
        """
        response = self.client.delete('/persons/999/')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
