from django.db import models
import datetime

# Create your models here.

all_lang = (
    ('c++', 'C++'),
    ('python', 'Python'),
    ('bash', 'Bash')
)

class Contest(models.Model):
    name = models.CharField(max_length=20)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.name}"

class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"

class Question(models.Model):
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
    ques = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="submissions")
    code = models.TextField()
    lang = models.CharField(max_length=10, choices=all_lang)


class Output(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="outputs")
    output = models.TextField()
    verdict = models.CharField(max_length=10)

