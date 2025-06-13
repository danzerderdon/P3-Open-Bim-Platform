from django.test import TestCase
from django.urls import reverse

class ProjectViewTest(TestCase):
    def test_project_list_view(self):
        url = reverse('project_list')  # Ersetze 'project_list' durch deinen URL-Namen
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/project_list.html')  # Passe Template-Namen an
