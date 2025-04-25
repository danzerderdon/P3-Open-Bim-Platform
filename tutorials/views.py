
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
from django.forms import modelformset_factory
from .models import Tutorial, TutorialSection, Quiz


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




from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import TutorialForm

@login_required
def create_tutorial(request):
    if request.method == 'POST':
        form = TutorialForm(request.POST, request.FILES)  # ✅ FILES hinzugefügt!
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
    tutorials = Tutorial.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'tutorials/create_landing.html', {'tutorials': tutorials})




#hate this part )=
from django.shortcuts import get_object_or_404






from django.contrib import messages  # falls du später im Template Feedback willst

@login_required
def edit_tutorial_sections(request, tutorial_id):
    tutorial = get_object_or_404(Tutorial, id=tutorial_id, created_by=request.user)

    SectionFormSet = modelformset_factory(
        TutorialSection,
        fields=('title', 'content', 'image', 'order'),
        extra=0,
        can_delete=True
    )

    if request.method == 'POST':
        formset = SectionFormSet(request.POST, request.FILES, queryset=TutorialSection.objects.filter(tutorial=tutorial))

        if formset.is_valid():
            instances = formset.save(commit=False)
            handled_ids = []

            for form in formset.forms:
                if form.cleaned_data.get('DELETE'):
                    continue

                instance = form.save(commit=False)
                instance.tutorial = tutorial

                if 'image' in form.cleaned_data and not form.cleaned_data.get('image'):
                    if form.instance.pk:
                        old_instance = TutorialSection.objects.get(pk=form.instance.pk)
                        instance.image = old_instance.image

                instance.save()
                handled_ids.append(instance.id)

            for obj in formset.deleted_objects:
                obj.delete()

            return redirect('create')  # redirect nur bei Erfolg
        else:
            # 👉 Fehlerausgabe in der Konsole
            print("❌ Formset ist NICHT valide:")
            for i, form in enumerate(formset.forms):
                if form.errors:
                    print(f"Formular {i} Fehler: {form.errors}")

            # 👉 Optional Feedback für User im Template (wenn du messages nutzt)
            messages.error(request, "Es gab ein Problem beim Speichern. Bitte überprüfe deine Eingaben.")
    else:
        formset = SectionFormSet(queryset=TutorialSection.objects.filter(tutorial=tutorial))

    return render(request, 'tutorials/edit_sections.html', {
        'formset': formset,
        'tutorial': tutorial
    })








@login_required
def delete_tutorial(request, tutorial_id):
    tutorial = get_object_or_404(Tutorial, id=tutorial_id, created_by=request.user)
    if request.method == 'POST':
        tutorial.delete()
        messages.success(request, 'Tutorial wurde gelöscht.')
        return redirect('create')
    return redirect('create')





from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TutorialForm
from .models import Tutorial

@login_required
def edit_tutorial_attributes(request, tutorial_id):
    tutorial = get_object_or_404(Tutorial, id=tutorial_id, created_by=request.user)

    if request.method == 'POST':
        form = TutorialForm(request.POST, request.FILES, instance=tutorial)  # ✅ FIX HIER
        if form.is_valid():
            form.save()
            return redirect('create')  # oder wohin du willst
    else:
        form = TutorialForm(instance=tutorial)

    return render(request, 'tutorials/edit_tutorial_attributes.html', {
        'form': form,
        'tutorial': tutorial
    })


from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Tutorial





from django.contrib import messages  # falls du später im Template Feedback willst

@login_required
def edit_tutorial_quiz(request, tutorial_id):
    tutorial = get_object_or_404(Tutorial, id=tutorial_id, created_by=request.user)

    QuizFormSet = modelformset_factory(
        Quiz,
        fields=('title', 'content', 'order', 'image',
                'answer_1', 'is_correct_1',
                'answer_2', 'is_correct_2',
                'answer_3', 'is_correct_3',
                'answer_4', 'is_correct_4',
                'answer_5', 'is_correct_5',
                ),
        extra=0,
        can_delete=True
    )

    if request.method == 'POST':
        formset = QuizFormSet(request.POST, request.FILES, queryset=Quiz.objects.filter(tutorial=tutorial))

        if formset.is_valid():
            instances = formset.save(commit=False)
            handled_ids = []

            for form in formset.forms:
                if form.cleaned_data.get('DELETE'):
                    continue

                instance = form.save(commit=False)
                instance.tutorial = tutorial


                instance.save()
                handled_ids.append(instance.id)

            for obj in formset.deleted_objects:
                obj.delete()

            return redirect('create')  # redirect nur bei Erfolg
        else:
            # 👉 Fehlerausgabe in der Konsole
            print("❌ Formset ist NICHT valide:")
            for i, form in enumerate(formset.forms):
                if form.errors:
                    print(f"Formular {i} Fehler: {form.errors}")

            # 👉 Optional Feedback für User im Template (wenn du messages nutzt)
            messages.error(request, "Es gab ein Problem beim Speichern. Bitte überprüfe deine Eingaben.")
    else:
        formset = QuizFormSet(queryset=Quiz.objects.filter(tutorial=tutorial))

    return render(request, 'tutorials/edit_questions.html', {
        'formset': formset,
        'tutorial': tutorial
    })