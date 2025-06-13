from django.test import TestCase
from core.models import Project

class ProjectModelTest(TestCase):
    def test_project_creation(self):
        project = Project.objects.create(name="Test Project")
        self.assertEqual(project.name, "Test Project")
        self.assertIsNotNone(project.created_at)
