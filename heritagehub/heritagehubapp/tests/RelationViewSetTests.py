from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from heritagehub.heritagehubapp.models import RelationModel
from heritagehub.heritagehubapp.models import PersonModel
from rest_framework import status


class RelationViewSetTests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='adminTest', password='azerty1234', email='adminTest@test.com')
        self.user2 = User.objects.create_user(
            username='adminTest2', password='azerty1234', email='adminTest2@test.com')
        self.client.force_authenticate(user=self.user)

        person_data = {
            "first_name": "test first_name",
            "last_name": "test last_name",
            "birth_date": "2000-08-07",
            "familly_id": None,
            "child_from_marriage": None
        }

        self.test_person = PersonModel.objects.create(
            created_by=self.user, **person_data)

        self.relation_data = {
            "person_id": self.test_person,
            "other_person_id": 4,
            "relation_type": "cousine"
        }

        self.test_relation = RelationModel.objects.create(
            created_by=self.user, **self.relation_data)

    def test_list_relations(self):
        """
        Test that the API endpoint for listing relations returns a 200 status code and non-empty data.
        """
        response = self.client.get('/relations/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_create_relation_authenticate_user(self):
        """
        Test that an authenticated user can create a new relation.
        """

        relation_data = {
            "person_id": 1,
            "other_person_id": 4,
            "relation_type": "cousine"
        }
        response = self.client.post(
            '/relations/', relation_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(RelationModel.objects.count(), 2)
        self.assertEquals(RelationModel.objects.last().created_by, self.user)
        self.assertEquals(
            RelationModel.objects.last().relation_type, relation_data['relation_type'])

    def test_create_relation_invalid_relation_type(self):
        """
        Test that a user can't create a relation without valid relation type
        """

        relation_data = {
            "person_id": 1,
            "other_person_id": 4,
            "relation_type": "invalid relation type"
        }
        response = self.client.post(
            '/relations/', relation_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_retreive_relation(self):
        """
        Test that an authenticated user can retrieve a relation
        """
        response = self.client.get(f'/relations/{self.test_relation.id}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['created_by'], self.user.id)
        self.assertEquals(response.data['relation_type'], "cousine")

    def test_partial_update_relation_authenticate_user(self):
        """
        Test that an authenticated user can partially update a relation, and 'created_by' and relation_type field are updated.
        """
        updated_data = {'created_by': self.user2.id,
                        'relation_type': 'cousin'}
        response = self.client.patch(
            f'/relations/{self.test_relation.id}/', updated_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.test_relation.refresh_from_db()
        self.assertEquals(self.test_relation.created_by.id,
                          updated_data["created_by"])
        self.assertEquals(self.test_relation.relation_type,
                          updated_data["relation_type"])

    def test_partial_update_with_invalid_relation_type(self):
        """
        Test that an authenticated user can't partially update a relation without a good relation_type
        """
        updated_data = {'created_by': self.user2.id,
                        'relation_type': 'invalid relation type'}
        response = self.client.patch(
            f'/relations/{self.test_relation.id}/', updated_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_destroy_relation_authenticated_user(self):
        """
        Test that an authenticated user can delete a relation and it no longer exists in the database.
        """
        response = self.client.delete(f'/relations/{self.test_relation.id}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        with self.assertRaises(RelationModel.DoesNotExist):
            RelationModel.objects.get(id=self.test_relation.id)

    def test_destroy_relation_noexistant(self):
        """
        Test that attempting to delete a non-existent relation returns a 404 Not Found status.
        """
        response = self.client.delete('/relations/999/')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
