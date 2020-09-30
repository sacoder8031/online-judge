from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.fields.related import OneToOneField

# Create your models here.

all_lang = (
    ('c++', 'C++'),
    ('python', 'Python'),
    ('bash', 'Bash')
)


class userdata(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userdata")
    correct = models.IntegerField(default=0)
    incorrect = models.IntegerField(default=0)


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
    timestamp = models.TimeField(auto_now=True)


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

    def __str__(self):
        return f"{self.id} {self.name}"


class Testcase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="testcases")
    testcase = models.TextField()
    answer = models.TextField()


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    ques = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="submissions")
    code = models.TextField()
    lang = models.CharField(max_length=10, choices=all_lang)
    verdict = models.CharField(max_length=10)