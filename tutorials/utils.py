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






import matplotlib
matplotlib.use('Agg')  # wichtig für Deployment ohne GUI
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from matplotlib.ticker import MaxNLocator


from .models import UserProgress


def generate_score_distribution(tutorial, current_user):
    progresses = UserProgress.objects.filter(tutorial=tutorial, score_percent__gte=50)
    scores = [p.score_percent for p in progresses]
    bins = np.arange(50, 105, 5)  # 50–100 in 5er-Schritten

    user_progress = progresses.filter(user=current_user, completed=True).first()
    user_score = user_progress.score_percent if user_progress else None

    # 🎨 Optisch modernisieren
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)  # höhere Auflösung

    # Histogramm mit zentrierten Balken
    ax.hist(scores, bins=bins, align='mid', color='#226D88', edgecolor='white', rwidth=0.85)

    # Achsenbeschriftungen
    ax.set_xlabel("Score", fontsize=12,fontweight='bold', fontname='Arial')
    ax.set_ylabel("Anzahl Nutzer",fontweight='bold', fontsize=12, fontname='Arial')
    # Y-Achse: nur ganze Zahlen, maximal 10 Ticks
    from math import ceil

    max_count = max(np.histogram(scores, bins=bins)[0])
    ymax = int(ceil(max_count / 2) * 2)

    ax.set_ylim(top=ymax)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True, nbins=10))



    #ax.set_title("Notenverteilung", fontsize=14, fontweight='bold', fontname='Arial')

    ax.set_xticks(bins)
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)

    # Vertikale Linie für Nutzer
    if user_score is not None:
        user_score_rounded = int(round(user_score))

        # Vertikale Linie (durchgehend bis unterhalb des Plots)
        ax.axvline(user_score, color='red', linewidth=5.0, ymin=0, ymax=1)

        # Text unterhalb des Plots, außerhalb des Plotbereichs
        ax.annotate(
            f'Dein Score: {user_score_rounded} %',
            xy=(user_score, 0),  # Linie endet an X-Achse
            xytext=(user_score, -0),  # Text deutlich unterhalb, außerhalb Plot
            textcoords='data',
            ha='center',
            fontsize=10,
            fontweight='bold',
            color='black',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='black')
        )

    # Keine schwarzen Ränder
    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.patch.set_facecolor('none')  # wichtig für transparenten oder sauberen Hintergrund

    # Grafik als base64 zurückgeben
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)

    return image_base64

