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
    program_versions = models.ManyToManyField(ProgramVersion, blank=True)

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
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.tutorial.title} – Schritt {self.order}: {self.title}"


class Question(models.Model):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    section = models.ForeignKey(TutorialSection, on_delete=models.CASCADE, null=True, blank=True)
    question_text = models.TextField()
    question_type = models.CharField(
        max_length=10,
        choices=[('mc', 'Multiple Choice'), ('dropdown', 'Dropdown')]
    )

    def __str__(self):
        return f"Frage: {self.question_text[:50]}"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    answer_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.answer_text} ({'✔' if self.is_correct else '❌'})"


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} – {self.tutorial.title} ({'Fertig' if self.completed else 'Nicht fertig'})"
