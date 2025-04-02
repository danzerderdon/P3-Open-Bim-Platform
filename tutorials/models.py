from django.db import models
from django.contrib.auth.models import User

class Program(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tutorial(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    keywords = models.CharField(max_length=200)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class TutorialSection(models.Model):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='tutorial_images/', blank=True, null=True)

class Question(models.Model):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.CharField(
        max_length=10,
        choices=[('mc', 'Multiple Choice'), ('dropdown', 'Dropdown')]
    )

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
