from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Tutorial
from django.forms import Textarea, TextInput

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


class RoleChangeForm(forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label="Neue Rolle auswählen",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
class TutorialForm(forms.ModelForm):
    class Meta:
        model = Tutorial
        fields = ['title', 'description', 'difficulty', 'category', 'program', 'keywords']
        widgets = {
            'keywords': Textarea(attrs={
                'rows': 3,
                'placeholder': 'Gib hier deine Keywords ein, z. B.: IFC, Modellierung, Koordination'
            }),
            'program': TextInput(attrs={
                'placeholder': 'Name des Programms (frei wählbar)'
            })
        }