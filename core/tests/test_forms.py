from django.test import TestCase
from core.forms import ProjectForm  # Bitte prüfen, ob der Pfad so stimmt

class ProjectFormTest(TestCase):
    def test_form_valid_data(self):
        form_data = {'name': 'Mein Projekt'}
        form = ProjectForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_no_data(self):
        form = ProjectForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
