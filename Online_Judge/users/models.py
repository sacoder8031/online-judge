from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.fields import NullBooleanField
from django.db.models.fields.related import OneToOneField
from django.utils.tree import Node
from jsonfield import JSONField
from typing_extensions import runtime

# Create your models here.

all_lang = (
    ('cpp', 'C++'),
    ('py', 'Python'),
    ('c', 'C')
)


class userdata(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userdata")
    correct = models.IntegerField(default=0)
    incorrect = models.IntegerField(default=0)
    runtime = models.IntegerField(default=0)
    timelimit = models.IntegerField(default=0)
    tags = JSONField(default={"isnull": True})
    notifications = JSONField(default={"isnull": True})

    def __str__(self):
        return f'{self.user}'


class Contest(models.Model):
    name = models.CharField(max_length=20)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    participants = models.ManyToManyField(User, related_name="contests")

    def __str__(self) -> str:
        return f"{self.name}"


class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    name = models.CharField(max_length=20)
    statement = models.TextField()
    contest = OneToOneField(Contest, on_delete=models.CASCADE, related_name="blog")
    date = models.DateField(auto_now=True)
    timestamp = models.TimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class Tag(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.name}"

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="questions")
    name = models.CharField(max_length=10)
    statement = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True, related_name="questions")
    contest = models.ForeignKey(Contest, blank=True, on_delete=models.CASCADE, related_name="questions")
    timelimit = models.DecimalField(max_digits=6, decimal_places=3, default=1)
    memlimit = models.IntegerField(default=128)

    def __str__(self):
        return f"{self.name}"


class Testcase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="testcases")
    testcase = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return f'{self.question.name}'


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    ques = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="submissions")
    code = models.TextField()
    lang = models.CharField(max_length=10, choices=all_lang)
    verdict = models.CharField(max_length=50, default="Queued...")

    def __str__(self):
        return f'{self.user} ----> {self.ques}'