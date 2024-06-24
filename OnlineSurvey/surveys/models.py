from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    profile_image_url = models.URLField()

    def __str__(self):
        return self.name


class Test(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Question(models.Model):
    SINGLE_CHOICE = 'single'
    MULTIPLE_CHOICE = 'multiple'
    TEXT_RESPONSE = 'text'

    QUESTION_TYPES = [
        (SINGLE_CHOICE, 'Single Choice'),
        (MULTIPLE_CHOICE, 'Multiple Choice'),
        (TEXT_RESPONSE, 'Text Response'),
    ]

    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Response(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    respondent = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Response by {self.respondent} to {self.test}"


class Answer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True)
    text_answer = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Answer to {self.question}"


class Result(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
    submitted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Result for {self.test} by {self.participant}"
