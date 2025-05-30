# tutorials/init_achievements.py
from tutorials.models import Achievement

ACHIEVEMENTS = [
    {"title": "Erstes Tutorial", "description": "Du hast dein erstes Tutorial abgeschlossen!"},
    {"title": "10 Tutorials", "description": "Du hast 10 Tutorials abgeschlossen!"},
    {"title": "Profilbild", "description": "Du hast ein Profilbild hochgeladen!"},
    {"title": "Top 3 Platzierung", "description": "Du gehörst zu den Top 3 im Ranking!"},
    {"title": "Perfektes Quiz", "description": "Du hast 100 % Score in einem Quiz erreicht!"},
]

def run():
    for ach in ACHIEVEMENTS:
        obj, created = Achievement.objects.get_or_create(title=ach["title"], defaults={"description": ach["description"]})
        if created:
            print(f"✅ Erstellt: {obj.title}")
        else:
            print(f"⚠️ Bereits vorhanden: {obj.title}")
