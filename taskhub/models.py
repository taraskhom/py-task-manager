from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name='worker'
    )


class TaskType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Task(models.Model):

    PRIORITY_CHOICES = [
        ('1', 'Urgent'),
        ('2', 'High Priority'),
        ('3', 'Medium Priority'),
        ('4', 'Low Priority')
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=1,
        choices=PRIORITY_CHOICES,
        default='3'
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name='task'
    )
    assignees = models.ManyToManyField(Worker, related_name='task')
    assigned_by = models.ForeignKey(
        Worker,
        on_delete=models.CASCADE,
        blank=True,
        related_name="assigned_task"
    )
