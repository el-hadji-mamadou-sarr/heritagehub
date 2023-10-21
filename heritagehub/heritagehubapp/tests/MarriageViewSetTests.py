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

        husband_data = {
            "first_name": "test first_name husband",
            "last_name": "test last_name husband",
            "birth_date": "2000-08-07",
            "familly_id": None,
            "child_from_marriage": None
        }
        wife_data = {
            "first_name": "test first_name wife",
            "last_name": "test last_name wife",
            "birth_date": "2000-08-07",
            "familly_id": None,
            "child_from_marriage": None
        }

        test_husband = PersonModel.objects.create(
            created_by=self.user, **husband_data)

        test_wife = PersonModel.objects.create(
            created_by=self.user, **wife_data)

        self.marriage_data = {
            "husband_id": test_husband,
            "wife_id": test_wife,
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
        Test that an authenticated user can create a new marriage.
        """

        marriage_data = {
            "husband_id": 1,
            "wife_id": 2,
            "marriage_date": "2022-08-07"
        }
        response = self.client.post(
            '/marriages/', marriage_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(MarriageModel.objects.count(), 2)
        self.assertEquals(MarriageModel.objects.last().created_by, self.user)
        self.assertEquals(MarriageModel.objects.last(
        ).husband_id.id, marriage_data['husband_id'])
        self.assertEquals(MarriageModel.objects.last().wife_id.id,
                          marriage_data['wife_id'])

    def test_retreive_marriage(self):
        """
        Test that an authenticated user can retrieve a marriage 
        """
        response = self.client.get(f'/marriages/{self.test_marriage.id}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['created_by'], self.user.id)
        self.assertEquals(
            response.data['husband_id'], self.marriage_data['husband_id'].id)
        self.assertEquals(response.data['wife_id'],
                          self.marriage_data['wife_id'].id)

    def test_partial_update_mariage_authenticate_user(self):
        """
        Test that an authenticated user can partially update a marriage, and 'created_by',husband_id and wife_id fields are updated.
        """
        updated_data = {'created_by': self.user2.id,
                        'marriage_date': "2023-08-14"}
        response = self.client.patch(
            f'/marriages/{self.test_marriage.id}/', updated_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.test_marriage.refresh_from_db()
        self.assertEquals(self.test_marriage.created_by.id,
                          updated_data['created_by'])
        self.assertEquals(self.test_marriage.marriage_date.strftime('%Y-%m-%d'),
                          updated_data['marriage_date'])

    def test_destroy_marriage_authenticated_user(self):
        """
        Test that an authenticated user can delete a marriage and it no longer exists in the database.
        """
        response = self.client.delete(f'/marriages/{self.test_marriage.id}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        with self.assertRaises(MarriageModel.DoesNotExist):
            MarriageModel.objects.get(id=self.test_marriage.id)

    def test_destroy_marriage_noexistant(self):
        """
        Test that attempting to delete a non-existent marriage returns a 404 Not Found status.
        """
        response = self.client.delete('/marriages/999/')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
