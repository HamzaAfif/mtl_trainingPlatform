from django.db import models
from django.contrib.auth.models import User

class QuestionnaireResult(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Assuming one set of answers per user
    favorite_team = models.CharField(max_length=10)
    favorite_topic = models.CharField(max_length=100)
    comfort_level = models.CharField(max_length=50)
    completed = models.BooleanField(default=False)  # Check if the user has completed the questionnaire

class DetailedAnswer(models.Model):
    result = models.ForeignKey(QuestionnaireResult, on_delete=models.CASCADE, related_name='answers')
    question = models.CharField(max_length=255)
    answer = models.TextField()
