from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from heritagehub.heritagehubapp.models import FamillyModel
from rest_framework import status

class FamillyViewSetTests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='adminTest', password='azerty1234', email='adminTest@test.com')
        self.client.force_authenticate(user=self.user)
        self.familly_data={}
        self.test_familly = FamillyModel.objects.create(created_by=self.user.id,**self.familly_data)

    def test_list_famillies(self):
        """
        Test that the API endpoint for listing posts returns a 200 status code and non-empty data.
        """
        response = self.client.get('/famillies/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_create_familly_authenticate_user(self):
        """
        Test that an authenticated user can create a new family.
        """
        response = self.client.post('/famillies/', self.familly_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(FamillyModel.objects.count(),2)
        self.assertEquals(FamillyModel.objects.last().created_by,self.user.id)  

    def test_retreive_familly(self):
        """
        Test that an authenticated user can retrieve a family and that the 'created_by' field matches the user's ID.
        """
        response = self.client.get(f'/famillies/{self.test_familly.id}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['created_by'], self.user.id)
    
    def test_partial_update_familly_authenticate_user(self):
        """
        Test that an authenticated user can partially update a family, and 'created_by' field is updated.
        """
        updated_data = {'created_by':2}
        response = self.client.patch(f'/famillies/{self.test_familly.id}/',updated_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.test_familly.refresh_from_db()
        self.assertEquals(self.test_familly.created_by, 2)

    def test_destroy_familly_authenticated_user(self):
        """
        Test that an authenticated user can delete a family and it no longer exists in the database.
        """
        response = self.client.delete(f'/famillies/{self.test_familly.id}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        with self.assertRaises(FamillyModel.DoesNotExist):
            FamillyModel.objects.get(id=self.test_familly.id)
    
    def test_destroy_familly_noexistant(self):
        """
        Test that attempting to delete a non-existent family returns a 404 Not Found status.
        """
        response = self.client.delete('/famillies/999/')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)