# tutorials/utils.py

from .models import UserProgress, Achievement, UserAchievement, QuizResult, UserProfile
from django.db.models import Count

def check_and_award_achievements(user):
    # 1. Erstes abgeschlossenes Tutorial
    if UserProgress.objects.filter(user=user, completed=True).count() >= 1:
        award(user, "Erstes Tutorial")

    # 2. 10 abgeschlossene Tutorials
    if UserProgress.objects.filter(user=user, completed=True).count() >= 10:
        award(user, "10 Tutorials")

    # 3. Profilbild hochgeladen
    profile = getattr(user, "userprofile", None)
    if profile and profile.profile_picture:
        award(user, "Profilbild")

    # 4. Top 3 Ranking
    top_users = (
        UserProgress.objects.filter(completed=True)
        .values("user")
        .annotate(total=Count("id"))
        .order_by("-total")[:3]
    )
    if any(u["user"] == user.id for u in top_users):
        award(user, "Top 3 Platzierung")

    # 5. Perfektes Quiz
    if QuizResult.objects.filter(user=user, score_percent=100.0).exists():
        award(user, "Perfektes Quiz")

    # 6. Serien-Master
    from .models import Tutorial
    series_names = Tutorial.objects.exclude(series__isnull=True).values_list("series", flat=True).distinct()

    for series in series_names:
        tutorials = Tutorial.objects.filter(series=series)
        if all(UserProgress.objects.filter(user=user, tutorial=t, completed=True).exists() for t in tutorials):
            title = f"{series}-Master"
            award(user, title, f"Alle Tutorials der Serie '{series}' abgeschlossen.")

def award(user, title, description=None):
    achievement = Achievement.objects.filter(title=title).first()
    if not achievement:
        achievement = Achievement.objects.create(title=title, description=description or "")

    # Nur einmalig vergeben
    UserAchievement.objects.get_or_create(user=user, achievement=achievement)
