from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class UserViewSetTests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='adminTest', password='azerty1234', email='adminTest@test.com')
        self.superuser = User.objects.create_superuser(
            username='superuser', password='azerty1234', email='superuser@test.com')
        self.client.force_authenticate(user=self.superuser)

    def test_list_users(self):
        """
        Test that the API endpoint for listing posts returns a 200 status code and non-empty data.
        """
        response = self.client.get('/users/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_register(self):
        """
        Test that a non user can create an account
        """

        user_data = {'username': 'newuser',
                     'email': 'newuser@newuser.com', 'password': 'secret'}
        response = self.client.post(
            '/users/', user_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(User.objects.count(), 3)
        self.assertEquals(User.objects.last().username, user_data['username'])

    def test_register_username_already_exists(self):
        """
        Test that a non user can't create account with the same username
        """

        user_data = {'username': 'adminTest',
                     'email': 'newuser@newuser.com', 'password': 'secret'}
        response = self.client.post(
            '/users/', user_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retreive_user(self):
        """
        Test that a superuser can retreive a user
        """
        response = self.client.get(f'/users/{self.user.id}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['username'], 'adminTest')
        self.assertEquals(response.data['email'], 'adminTest@test.com')
