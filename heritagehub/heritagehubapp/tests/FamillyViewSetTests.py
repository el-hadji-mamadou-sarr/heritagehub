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

    