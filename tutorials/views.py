
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
from .models import Tutorial

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
    show_archived = request.GET.get('show_archived') == '1'

    if show_archived:
        tutorials = Tutorial.objects.filter(created_by=request.user).order_by('-created_at')
    else:
        tutorials = Tutorial.objects.filter(created_by=request.user).exclude(series='Archiviert').order_by('-created_at')

    return render(request, 'tutorials/create_landing.html', {
        'tutorials': tutorials,
        'show_archived': show_archived
    })


#hate this part )=
from django.shortcuts import get_object_or_404






from django.contrib import messages  # falls du später im Template Feedback willst
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.forms import modelformset_factory
from django.contrib import messages
from .models import Tutorial, TutorialSection


@login_required
def edit_tutorial_sections(request, tutorial_id):
    tutorial = get_object_or_404(Tutorial, id=tutorial_id, created_by=request.user)

    SectionFormSet = modelformset_factory(
        TutorialSection,
        fields=('title', 'content', 'image', 'video', 'order'),
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

                # ✅ Bild wirklich löschen, wenn "Bild entfernen" aktiviert wurde
                if form.cleaned_data.get('image_clear') and form.instance.image:
                    form.instance.image.delete(save=False)
                    form.instance.image = None

                # ✅ Video löschen
                if form.cleaned_data.get('video_clear') and form.instance.video:
                    form.instance.video.delete(save=False)
                    form.instance.video = None

                instance.save()
                handled_ids.append(instance.id)

            for obj in formset.deleted_objects:
                obj.delete()

            return redirect('create')  # redirect nur bei Erfolg
        else:
            print("❌ Formset ist NICHT valide:")
            for i, form in enumerate(formset.forms):
                if form.errors:
                    print(f"Formular {i} Fehler: {form.errors}")
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

from django.views.generic import ListView
from .models import Tutorial
from django.db.models import Avg
from .models import TutorialRating


class TutorialListView(ListView):
    model = Tutorial
    template_name = 'tutorial_list.html'
    context_object_name = 'tutorials'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        # Zeigt nur Tutorials, die NICHT archiviert sind
        return Tutorial.objects.exclude(series='Archiviert').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tutorials_with_avg = []
        for tutorial in context['tutorials']:
            avg_rating = TutorialRating.objects.filter(tutorial=tutorial).aggregate(avg=Avg('rating'))['avg']
            tutorial.avg_rating = round(avg_rating or 0)
            tutorials_with_avg.append(tutorial)

        context['tutorials'] = tutorials_with_avg
        return context


from django.views.generic.detail import DetailView
from .models import Tutorial, UserProgress
from .utils import generate_score_distribution








from django.views.generic.detail import DetailView
from django.shortcuts import redirect
from .models import Tutorial, UserProgress, TutorialRating
from .forms import RatingForm
from .utils import generate_score_distribution

class TutorialDetailView(DetailView):
    model = Tutorial
    template_name = 'tutorials/tutorial_detail.html'
    context_object_name = 'tutorial'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tutorial = self.get_object()
        user = self.request.user

        # Schlüsselwörter vorbereiten
        context["keywords"] = [kw.strip() for kw in tutorial.keywords.split(",")] if tutorial.keywords else []

        # Anzahl Schritte & Quizfragen
        context["step_count"] = tutorial.sections.count()
        context["quiz_question_count"] = tutorial.quiz.count()

        # ⬇ Durchschnittlicher Score aller abgeschlossenen User
        avg_score = (
            tutorial.userprogress_set
            .filter(completed=True)
            .aggregate(Avg('score_percent'))['score_percent__avg']
        )

        context["avg_score_percent"] = round(avg_score, 1) if avg_score else None

        # Score-Chart nur für eingeloggte User mit abgeschlossenem Fortschritt
        if user.is_authenticated:
            try:
                progress = UserProgress.objects.get(user=user, tutorial=tutorial)
                if progress.completed:
                    context["score_chart"] = generate_score_distribution(tutorial, user)
                else:
                    context["score_chart"] = None
            except UserProgress.DoesNotExist:
                context["score_chart"] = None

            # Bewertungsformular vorbereiten (nur einmal bewertbar)
            existing_rating = TutorialRating.objects.filter(user=user, tutorial=tutorial).first()
            context["rating_form"] = RatingForm(instance=existing_rating)
        else:
            context["score_chart"] = None
            context["rating_form"] = None

        # Alle Bewertungen für Anzeige
        context["ratings"] = tutorial.ratings.select_related("user").order_by("-created_at")

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.user.is_authenticated:
            return redirect("login")

        form = RatingForm(request.POST)
        if form.is_valid():
            # Update oder erstelle Bewertung für aktuellen User
            TutorialRating.objects.update_or_create(
                user=request.user,
                tutorial=self.object,
                defaults=form.cleaned_data
            )

        return redirect("tutorial-detail", pk=self.object.pk)







from django.shortcuts import get_object_or_404, redirect, render
from .models import Tutorial, TutorialSection

def tutorial_step(request, tutorial_id, step_order):
    tutorial = get_object_or_404(Tutorial, id=tutorial_id)
    steps = tutorial.sections.all()
    total = steps.count()
    has_quiz = tutorial.quiz.exists()

    # aktueller Schritt
    step = get_object_or_404(TutorialSection, tutorial=tutorial, order=step_order)

    # progress in Prozent (Vorher-Schritt)
    # z. B. step_order = 3 von total=5 → (3-1)/5*100 = 40
    progress = int((step_order - 1) / total * 100)

    # Einen Schritt zurück: (step_order-2)/total*100, aber nie <0
    if step_order > 1:
        prev_progress = int((step_order - 2) / total * 100)
    else:
        prev_progress = 0

    return render(request, 'tutorials/step_by_step.html', {
        'tutorial': tutorial,
        'steps': steps,
        'step': step,
        'prev_order': step_order > 1 and step_order - 1 or None,
        'next_order': step_order < total and step_order + 1 or None,
        'progress': progress,
        'prev_progress': prev_progress,
        'active_page': 'tutorials',
        'has_quiz': has_quiz,  # 👈 HINZUGEFÜGT
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Tutorial

@login_required
def tutorial_all_steps(request, tutorial_id):
    tutorial = get_object_or_404(Tutorial, id=tutorial_id)
    steps = tutorial.sections.all()
    return render(request, 'tutorials/tutorial_all_steps.html', {
        'tutorial': tutorial,
        'steps': steps,
        'active_page': 'tutorials',
    })

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Tutorial, Quiz, QuizResult, UserProgress
from django.contrib.auth.decorators import login_required

@login_required
def start_quiz(request, tutorial_id):
    tutorial = get_object_or_404(Tutorial, id=tutorial_id)
    return redirect('quiz_question', tutorial_id=tutorial.id, question_order=1)

@login_required
def quiz_question(request, tutorial_id, question_order):
    tutorial = get_object_or_404(Tutorial, id=tutorial_id)
    question = get_object_or_404(Quiz, tutorial=tutorial, order=question_order)
    questions = Quiz.objects.filter(tutorial=tutorial).count()
    progress = int((question_order - 1) / questions * 100)

    # Hole vorherige Antworten aus der Session
    if 'answers' not in request.session:
        request.session['answers'] = {}

    if request.method == 'POST':
        selected = request.POST.getlist('selected_answers')
        request.session['answers'][str(question_order)] = selected
        request.session.modified = True

        if question_order < questions:
            return redirect('quiz_question', tutorial_id=tutorial.id, question_order=question_order + 1)
        else:
            return redirect('quiz_result', tutorial_id=tutorial.id)

    # Dynamisch nur gefüllte Antworten anzeigen
    answers = []
    for i in range(1, 6):
        answer = getattr(question, f'answer_{i}')
        if answer:
            answers.append({'text': answer, 'value': i})

    # NEU: Alle Fragen laden für die Sidebar
    quiz_list = Quiz.objects.filter(tutorial=tutorial).order_by('order')

    return render(request, 'tutorials/quiz_question.html', {

        'tutorial': tutorial,
        'quiz': question,
        'answers': answers,
        'order': question_order,
        'total': questions,
        'progress': progress,
        'quiz_list': quiz_list,

    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Tutorial, Quiz, QuizResult, UserProgress
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Tutorial, Quiz, QuizResult, UserProgress

@login_required
def quiz_result(request, tutorial_id):
    tutorial = get_object_or_404(Tutorial, id=tutorial_id)
    questions = Quiz.objects.filter(tutorial=tutorial)
    user_answers = request.session.get('answers', {})

    correct = 0
    total = questions.count()

    for q in questions:
        user_answer_list = user_answers.get(str(q.order), [])
        if not isinstance(user_answer_list, list):
            user_answer_list = [user_answer_list]

        correct_answers = [
            str(i) for i in range(1, 6)
            if getattr(q, f'is_correct_{i}')
        ]

        if set(user_answer_list) == set(correct_answers):
            correct += 1

    score = round((correct / total) * 100, 2) if total > 0 else 0.0

    if score >= 50:
        # Ergebnis speichern
        QuizResult.objects.update_or_create(
            user=request.user,
            tutorial=tutorial,
            defaults={
                'correct_answers': correct,
                'total_questions': total,
                'score_percent': score
            }
        )

        progress, _ = UserProgress.objects.get_or_create(
            user=request.user,
            tutorial=tutorial
        )
        progress.score_percent = score
        progress.completed = True
        progress.completed_at = timezone.now()  # ✅ Zeitstempel setzen
        progress.save()

    # Session aufräumen
    request.session.pop('answers', None)

    return render(request, 'tutorials/result.html', {
        'tutorial': tutorial,
        'score': score,
        'correct': correct,
        'total': total
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import UserProgress

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Tutorial, UserProgress
from django.contrib.auth.models import User
from django.db.models import Count, Q

from .models import UserProfile       # 👈 Import hinzufügen
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Count, Q
from .models import Tutorial, UserProgress, UserProfile
from .forms import ProfileForm  # ⬅ deine Form importieren
from .utils import check_and_award_achievements
from .models import UserAchievement  # falls noch nicht importiert

@login_required
def dashboard_view(request):
    # UserProfile holen oder erstellen
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    # Checke Achievements bei jedem Dashboard-Aufruf
    check_and_award_achievements(request.user)

    # Profilformular verarbeiten
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)

    # Fortschrittseinträge
    progress_entries = UserProgress.objects.filter(
        user=request.user, completed=True
    ).select_related('tutorial').order_by('-completed_at')

    # Serienübersicht
    all_series = Tutorial.objects.filter(
        userprogress__user=request.user
    ).values_list('series', flat=True).distinct()

    selected_series = request.GET.get('series')
    tutorials_in_series = Tutorial.objects.filter(series=selected_series).order_by('created_at') if selected_series else []

    # Fortschritts-Map
    progress_map = {
        p.tutorial.id: p for p in UserProgress.objects.filter(user=request.user)
    }

    total = len(tutorials_in_series)
    completed_count = sum(1 for t in tutorials_in_series if t.id in progress_map)
    open_count = total - completed_count

    if completed_count > 0:
        score_sum = sum(progress_map[t.id].score_percent for t in tutorials_in_series if t.id in progress_map)
        average_score = score_sum / completed_count
    else:
        average_score = 0

    percent_completed = int(100 * completed_count / total) if total > 0 else 0

    # Ranking
    user_rankings = (
        User.objects
        .annotate(completed_count=Count('userprogress', filter=Q(userprogress__completed=True)))
        .order_by('-completed_count', 'username')
    )

    current_user_rank = next(
        (i + 1 for i, u in enumerate(user_rankings) if u.id == request.user.id),
        None
    )
    current_user_completed = next(
        (u.completed_count for u in user_rankings if u.id == request.user.id),
        0
    )

    # Top 5
    top_users = (
        User.objects
        .annotate(tutorial_count=Count('userprogress', filter=Q(userprogress__completed=True)))
        .order_by('-tutorial_count', 'username')[:5]
    )



    user_achievements = UserAchievement.objects.filter(user=request.user).select_related('achievement')

    return render(request, 'tutorials/dashboard.html', {
        'form': form,  # ⬅ wichtig!
        'progress_entries': progress_entries,
        'series_list': all_series,
        'selected_series': selected_series,
        'tutorials_in_series': tutorials_in_series,
        'progress_map': progress_map,
        'completed_count': completed_count,
        'open_count': open_count,
        'average_score': average_score,
        'percent_completed': percent_completed,
        'current_user_rank': current_user_rank,
        'current_user_completed': current_user_completed,
        'top_users': top_users,
        'achievements': [ua.achievement for ua in user_achievements],
    })

from django.shortcuts import render, get_object_or_404
from .models import Tutorial, UserProgress

def completed_users_view(request, tutorial_id):
    tutorial = get_object_or_404(Tutorial, id=tutorial_id)
    completed_users = UserProgress.objects.filter(tutorial=tutorial, completed=True).select_related('user')

    return render(request, 'tutorials/completed_users.html', {
        'tutorial': tutorial,
        'completed_users': completed_users
    })

from django.shortcuts import render, get_object_or_404
from .models import Tutorial, UserProgress

def print_certificate(request, tutorial_id):
    tutorial = get_object_or_404(Tutorial, id=tutorial_id)
    user = request.user
    progress = UserProgress.objects.filter(user=user, tutorial=tutorial).first()

    return render(request, 'tutorials/certificate_print.html', {
        'tutorial': tutorial,
        'user': user,
        'progress': progress
    })

from django.http import JsonResponse
from .models import TutorialNote

@login_required
def save_note_ajax(request, tutorial_id):
    if request.method == 'POST':
        content = request.POST.get('content', '')
        note, _ = TutorialNote.objects.get_or_create(user=request.user, tutorial_id=tutorial_id)
        note.content = content
        note.save()
        return JsonResponse({'status': 'saved'})
    return JsonResponse({'status': 'error'}, status=400)


from django.http import JsonResponse
from .models import TutorialNote, TutorialSection
from django.contrib.auth.decorators import login_required

@login_required
def get_note_ajax(request, tutorial_id):
    note, _ = TutorialNote.objects.get_or_create(user=request.user, tutorial_id=tutorial_id)

    if "<u>Schritt" not in note.content:
        sections = TutorialSection.objects.filter(tutorial_id=tutorial_id).order_by('order')
        template_content = ""

        for section in sections:
            template_content += (
                f"<p><strong><u>Schritt {section.order}: {section.title}</u></strong></p>"
                f"<p>&nbsp;&nbsp;&nbsp;• </p><br><br>"
            )

        note.content = template_content + note.content
        note.save()

    return JsonResponse({'content': note.content})

from django.db.models import Max
from django.utils.text import slugify

@login_required
def archive_tutorial(request, tutorial_id):
    tutorial = get_object_or_404(Tutorial, id=tutorial_id, created_by=request.user)
    tutorial.series = "Archiviert"
    tutorial.save()
    return redirect('create')  # Zur Landingpage zurück


@login_required
def revision_tutorial(request, tutorial_id):
    original = get_object_or_404(Tutorial, id=tutorial_id, created_by=request.user)

    # Bestimme neue Version
    base_title = original.title
    if 'v' in base_title and base_title.split('v')[-1].isdigit():
        version = int(base_title.split('v')[-1]) + 1
        new_title = 'v'.join(base_title.split('v')[:-1]) + f'v{version}'
    else:
        new_title = base_title + ' v2'

    # Kopiere das Tutorial
    new_tutorial = Tutorial.objects.create(
        title=new_title,
        description=original.description,
        keywords=original.keywords,
        program=original.program,
        program_versions=original.program_versions,
        difficulty=original.difficulty,
        thumbnail=original.thumbnail,
        screenshot=original.screenshot,
        attachments=original.attachments,
        series=original.series,
        created_by=request.user
    )

    # Kopiere die Schritte
    for section in original.sections.all():
        TutorialSection.objects.create(
            tutorial=new_tutorial,
            title=section.title,
            content=section.content,
            image=section.image,
            video=section.video,
            order=section.order
        )

    # Kopiere Quizfragen
    for quiz in original.quiz.all():
        Quiz.objects.create(
            tutorial=new_tutorial,
            title=quiz.title,
            content=quiz.content,
            image=quiz.image,
            order=quiz.order,
            answer_1=quiz.answer_1,
            is_correct_1=quiz.is_correct_1,
            answer_2=quiz.answer_2,
            is_correct_2=quiz.is_correct_2,
            answer_3=quiz.answer_3,
            is_correct_3=quiz.is_correct_3,
            answer_4=quiz.answer_4,
            is_correct_4=quiz.is_correct_4,
            answer_5=quiz.answer_5,
            is_correct_5=quiz.is_correct_5
        )

    return redirect('edit_tutorial_sections', tutorial_id=new_tutorial.id)
