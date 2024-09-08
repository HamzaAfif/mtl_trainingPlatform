from django.db import models
from django.contrib.auth.models import User

class QuestionnaireResult(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_team = models.CharField(max_length=10, blank=True)  # Allow empty strings
    favorite_topic = models.CharField(max_length=100, blank=True)  # Allow empty strings
    comfort_level = models.CharField(max_length=50, blank=True)  # Allow empty strings
    completed = models.BooleanField(default=False)

class DetailedAnswer(models.Model):
    result = models.ForeignKey(QuestionnaireResult, on_delete=models.CASCADE, related_name='answers')
    question = models.CharField(max_length=255)
    answer = models.TextField()
