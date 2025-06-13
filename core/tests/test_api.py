from django.test import TestCase
from django.urls import reverse

class ProjectAPITest(TestCase):
    def test_projects_api_list(self):
        url = reverse('projects-list')  # URL-Name deines API-Endpunkts
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
