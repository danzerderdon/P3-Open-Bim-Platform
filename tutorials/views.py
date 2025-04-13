
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from .forms import UserRegisterForm
from .forms import RoleChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TutorialForm
from .models import Tutorial, TutorialSection
from django.forms import modelformset_factory


# Registrierung
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Rolle aus dem Formular holen und Gruppe zuweisen
            role = form.cleaned_data['role']
            group = Group.objects.get(name=role)
            user.groups.add(group)

            login(request, user)
            return redirect('/')
    else:
        form = UserRegisterForm()

    return render(request, 'tutorials/register.html', {'form': form})

# Startseite
def home(request):
    return render(request, 'tutorials/home.html')

# Logout-View
def logout_view(request):
    logout(request)
    return redirect('home')  # Weiterleitung zur home seite

# Passwort ändern – eigene View
@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Wichtig, um eingeloggt zu bleiben
            messages.success(request, 'Dein Passwort wurde erfolgreich geändert.')
            return redirect('passdone')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'registration/password_change_form.html', {'form': form})

@login_required
def password_change_done(request):
    return render(request, 'registration/password_change_done.html')

@login_required
def change_role_view(request):
    if request.method == 'POST':
        form = RoleChangeForm(request.POST)
        if form.is_valid():
            new_role = form.cleaned_data['role']

            # Alte Rollen entfernen (optional: je nach Logik)
            request.user.groups.clear()

            # Neue Rolle hinzufügen
            request.user.groups.add(new_role)

            messages.success(request, 'Deine Rolle wurde geändert.')
            return redirect('home')
    else:
        form = RoleChangeForm()

    return render(request, 'registration/change_role.html', {'form': form})

from django.http import HttpResponse

@login_required
def create_tutorial(request):
    if request.method == 'POST':
        form = TutorialForm(request.POST)
        if form.is_valid():
            print("✅ Formular ist valide.")

            tutorial = form.save(commit=False)
            tutorial.created_by = request.user
            tutorial.save()

            # 👉 Debug-Ausgaben:
            print(f"🎯 Tutorial wurde gespeichert mit ID: {tutorial.id}")
            print(f"👤 Ersteller: {tutorial.created_by} | Aktueller User: {request.user}")

            return redirect('edit_tutorial_sections', tutorial_id=tutorial.id)
        else:
            print("❌ Formular ist NICHT valide:")
            print(form.errors.as_text())
    else:
        form = TutorialForm()

    return render(request, 'tutorials/create_tutorial.html', {'form': form})

@login_required
def tutorial_create_landing(request):
    return render(request, 'tutorials/create_landing.html')

@login_required
def edit_tutorial_sections(request, tutorial_id):
    tutorial = Tutorial.objects.get(id=tutorial_id, created_by=request.user)

    SectionFormSet = modelformset_factory(
        TutorialSection,
        fields=('title', 'content', 'image', 'order'),
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        formset = SectionFormSet(request.POST, request.FILES, queryset=TutorialSection.objects.filter(tutorial=tutorial))
        if formset.is_valid():
            sections = formset.save(commit=False)
            for section in sections:
                section.tutorial = tutorial
                section.save()
            # Gelöschte Schritte entfernen
            for obj in formset.deleted_objects:
                obj.delete()
            return redirect('dashboard')  # Oder zu einer nächsten Seite
    else:
        formset = SectionFormSet(queryset=TutorialSection.objects.filter(tutorial=tutorial))

    return render(request, 'tutorials/edit_sections.html', {'formset': formset, 'tutorial': tutorial})