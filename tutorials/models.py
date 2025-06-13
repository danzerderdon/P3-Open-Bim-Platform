from django.db import models
from django.contrib.auth.models import User



class ProgramVersion(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tutorial(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    keywords = models.CharField(
        max_length=200,
        help_text="Kommagetrennt, z. B. IFC, Modellierung, BIM"
    )

    program = models.CharField(
        max_length=100,
        help_text="Z. B. Revit, ArchiCAD, Solibri"
    )
    program_versions = models.CharField(
        max_length=200,
        blank=True,
        help_text="Mehrere Versionen kommagetrennt angeben, z. B. 2021, 2022"
    )

    difficulty = models.CharField(
        max_length=20,
        choices=[
            ('leicht', 'Leicht'),
            ('mittel', 'Mittel'),
            ('schwer', 'Schwer'),
            ('expert', 'Expertenmodus')
        ],
        default='mittel'
    )

    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    screenshot = models.ImageField(upload_to='screenshots/', null=True, blank=True)
    attachments = models.FileField(upload_to='attachments/', null=True, blank=True)

    series = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Optional: Titel der Tutorial-Serie"
    )

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TutorialScreenshot(models.Model):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name="screenshots")
    image = models.ImageField(upload_to='screenshots/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Screenshot für: {self.tutorial.title}"


class TutorialSection(models.Model):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name="sections")
    title = models.CharField(max_length=200, default="Schritt")
    content = models.TextField()
    image = models.ImageField(upload_to='tutorial_images/', blank=True, null=True)
    video = models.FileField(upload_to='tutorial_videos/', blank=True, null=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.tutorial.title} – Schritt {self.order}: {self.title}"



class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)

    # Neues Feld: Score in Prozent
    score_percent = models.FloatField(default=0.0)

    # Flag, ob Quiz & Tutorial abgeschlossen
    completed = models.BooleanField(default=False)

    # Zeitstempel der letzten vollständigen Bearbeitung
    completed_at = models.DateTimeField(null=True, blank=True)

    # Optional: Anzahl der Versuche (z. B. für Statistik)
    attempts = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'tutorial')

    def __str__(self):
        status = "✅" if self.completed else "❌"
        return f"{self.user.username} – {self.tutorial.title} {status} ({self.score_percent:.1f} %)"



class Quiz(models.Model):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name="quiz")
    title = models.CharField(max_length=200, default="Schritt")
    content = models.TextField()
    image = models.ImageField(upload_to='tutorial_images/', blank=True, null=True)
    order = models.PositiveIntegerField(default=1)

    # Antwortmöglichkeiten
    answer_1 = models.CharField(max_length=255, blank=True)
    is_correct_1 = models.BooleanField(default=False)

    answer_2 = models.CharField(max_length=255, blank=True)
    is_correct_2 = models.BooleanField(default=False)

    answer_3 = models.CharField(max_length=255, blank=True)
    is_correct_3 = models.BooleanField(default=False)

    answer_4 = models.CharField(max_length=255, blank=True)
    is_correct_4 = models.BooleanField(default=False)

    answer_5 = models.CharField(max_length=255, blank=True)
    is_correct_5 = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.tutorial.title} – Frage {self.order}: {self.title}"

class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    correct_answers = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    score_percent = models.FloatField(default=0.0)
    last_attempt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} – {self.tutorial.title} ({self.score_percent:.1f}%)"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)  # 🔥 NEU: Bio-Feld
    dummy = models.BooleanField(default=False)

    def __str__(self):
        return f"Profil von {self.user.username}"

# models.py
from django.db import models
from django.contrib.auth.models import User

class Achievement(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='achievement_icons/', blank=True, null=True)

    def __str__(self):
        return self.title

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'achievement')

    def __str__(self):
        return f"{self.user.username} – {self.achievement.title}"

from django.db import models
from django.contrib.auth.models import User

class TutorialRating(models.Model):
    tutorial = models.ForeignKey('Tutorial', related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tutorial', 'user')

    def __str__(self):
        return f"{self.user} – {self.rating}★"

from django.db import models
from django.contrib.auth.models import User
from .models import Tutorial

class TutorialNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'tutorial')
