from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=50)


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="worker")


class TaskType(models.Model):
    name = models.CharField(max_length=50)


class Task(models.Model):

    PRIORITY_CHOICES = [
        ('U', 'Urgent'),
        ('H', 'High Priority'),
        ('M', 'Medium Priority'),
        ('L', 'Low Priority'),
        ('N', 'Normal'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='N')
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, related_name="task")
    assignees = models.ManyToManyField(Worker, related_name="task")
