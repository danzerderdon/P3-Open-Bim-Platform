from django.test import TestCase
from django.urls import reverse
from core.models import Project

class ProjectIntegrationTest(TestCase):
    def test_create_project_via_form_and_view(self):
        form_data = {'name': 'Integration Project'}

        # POST-Daten an View senden (angenommen URL-Name ist 'project_create')
        url = reverse('project_create')
        response = self.client.post(url, data=form_data)

        # Prüfen, ob Redirect (Erfolg) zurückkommt
        self.assertEqual(response.status_code, 302)

        # Prüfen, ob das Projekt wirklich in der DB ist
        project = Project.objects.filter(name='Integration Project').first()
        self.assertIsNotNone(project)
