from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import UserRegisterForm

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
    return redirect('login')  # Weiterleitung zur Login-Seite

# Passwort ändern – eigene View
@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Wichtig, um eingeloggt zu bleiben
            messages.success(request, 'Dein Passwort wurde erfolgreich geändert.')
            return redirect('password_change_done')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'registration/password_change_form.html', {'form': form})

from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import UserRegisterForm

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
    return redirect('login')  # Weiterleitung zur Login-Seite

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
