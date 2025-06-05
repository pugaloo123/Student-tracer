from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Group(models.Model):
    name = models.CharField(max_length=50)
    subjects = models.ManyToManyField('Subject', related_name='groups', blank=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return self.name


class Subject(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


GRADE_CHOICES = [
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
]

class Grade(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    grade = models.IntegerField(choices=GRADE_CHOICES)

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.grade}"
