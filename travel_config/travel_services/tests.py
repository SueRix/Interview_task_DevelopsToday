# travel_services/tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from .models import TravelProject, Place


class TravelProjectAPITests(APITestCase):

    def setUp(self):
        self.project_data = {
            "name": "Test Trip to Chicago",
            "description": "Testing the API",
            "start_date": "2024-10-10"
        }
        self.project = TravelProject.objects.create(**self.project_data)

        # Helper URLs
        self.project_list_url = '/api/projects/'
        self.project_detail_url = f'/api/projects/{self.project.id}/'
        self.place_list_url = f'/api/projects/{self.project.id}/places/'

    def test_create_project_without_places(self):
        response = self.client.post(self.project_list_url, {
            "name": "Paris Trip"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TravelProject.objects.count(), 2)

    @patch('travel_services.services.requests.get')
    def test_create_project_with_valid_places(self, mock_get):
        # Mock external API to always return 200 OK
        mock_get.return_value.status_code = 200

        payload = {
            "name": "Art Tour",
            "places": [
                {"external_id": "111", "notes": "First place"},
                {"external_id": "222", "notes": "Second place"}
            ]
        }
        response = self.client.post(self.project_list_url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Place.objects.count(), 2)
        # Ensure the external API was called twice
        self.assertEqual(mock_get.call_count, 2)

    @patch('travel_services.services.requests.get')
    def test_add_invalid_place_fails(self, mock_get):
        # Mock external API to simulate a 404 Not Found error
        mock_get.return_value.status_code = 404

        response = self.client.post(self.place_list_url, {
            "external_id": "invalid_999"
        }, format='json')

        # Expect 400 Bad Request due to validation failure
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Place.objects.count(), 0)

    def test_delete_project_with_visited_places_fails(self):
        # Add a visited place to the existing project
        Place.objects.create(
            project=self.project,
            external_id="123",
            is_visited=True
        )

        # Attempt to delete the project
        response = self.client.delete(self.project_detail_url)

        # Ensure deletion is blocked
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TravelProject.objects.count(), 1)

    def test_is_completed_property(self):
        # Create two places for the project
        place1 = Place.objects.create(project=self.project, external_id="111")
        place2 = Place.objects.create(project=self.project, external_id="222")

        # Project should not be completed initially
        response = self.client.get(self.project_detail_url)
        self.assertFalse(response.data['is_completed'])

        # Mark first place as visited
        place1.is_visited = True
        place1.save()

        response = self.client.get(self.project_detail_url)
        self.assertFalse(response.data['is_completed'])

        # Mark second place as visited
        place2.is_visited = True
        place2.save()

        # Project should now be marked as completed
        response = self.client.get(self.project_detail_url)
        self.assertTrue(response.data['is_completed'])

    @patch('travel_services.services.requests.get')
    def test_max_places_limit(self, mock_get):
        # Mock external API to return 200 OK
        mock_get.return_value.status_code = 200

        # Fill the project with 10 places directly
        for i in range(10):
            Place.objects.create(project=self.project, external_id=str(i))

        # Try to add the 11th place via API
        response = self.client.post(self.place_list_url, {
            "external_id": "999"
        }, format='json')

        # Should return validation error
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)