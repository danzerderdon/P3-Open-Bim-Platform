from django import forms
from django.contrib.auth.models import User, Group
from .models import Tutorial, TutorialScreenshot, ProgramVersion
from django.forms import Textarea, TextInput, ClearableFileInput, Select, CheckboxSelectMultiple


# Registrierung
class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    ROLE_CHOICES = [
        ('BIM Expert', 'BIM Expert'),
        ('Student', 'Student')
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']


# Rollenwechsel
class RoleChangeForm(forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label="Neue Rolle auswählen",
        widget=forms.Select(attrs={'class': 'form-control'})
    )


# Tutorial-Formular
class TutorialForm(forms.ModelForm):
    class Meta:
        model = Tutorial
        fields = [
            'title',
            'description',
            'difficulty',
            'program',
            'program_versions',
            'keywords',
            'thumbnail',
            'screenshot',
            'attachments',
            'series',
        ]
        widgets = {
            'title': TextInput(attrs={'placeholder': 'Titel des Tutorials'}),
            'description': Textarea(attrs={'placeholder': 'Kurze Beschreibung des Tutorials'}),
            'difficulty': Select(),
            'program': TextInput(attrs={'placeholder': 'Name des Programms'}),
            'program_versions': TextInput(attrs={
    'placeholder': 'z. B. 2021, 2022, 2023'
}),

            'keywords': Textarea(attrs={
                'rows': 3,
                'placeholder': 'Gib hier deine Keywords ein, z. B.: IFC, Modellierung, Koordination'
            }),
            'thumbnail': ClearableFileInput(attrs={'accept': 'image/*'}),
            'screenshot': ClearableFileInput(attrs={'accept': 'image/*'}),
            'attachments': ClearableFileInput(attrs={'multiple': False}),
            'series': TextInput(attrs={'placeholder': 'Optional: Serie wie "Solibri Basics"'}),
        }


# Zusätzliche Screenshots für Prozessdiagramme
class TutorialScreenshotForm(forms.ModelForm):
    class Meta:
        model = TutorialScreenshot
        fields = ['image', 'caption']
        widgets = {
            'image': ClearableFileInput(attrs={'accept': 'image/*'}),
            'caption': TextInput(attrs={'placeholder': 'Beschreibung (optional)'})
        }
