from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django_select2.forms import Select2MultipleWidget

from .models import Task, Position, TaskType, Worker


class WorkerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'position'
        )


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['username', 'first_name', 'last_name', 'email', 'position']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'name',
            'description',
            'deadline',
            'priority',
            'task_type',
            'assignees'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Task Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Task Description',
                'rows': 3
            }),
            'deadline': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'task_type': forms.Select(attrs={'class': 'form-control'}),
        }

    assignees = forms.ModelMultipleChoiceField(
        queryset=Worker.objects,
        widget=Select2MultipleWidget
    )

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')

        if deadline and deadline < now().date():
            raise ValidationError('Deadline cannot be in the past!')

        return deadline


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Position Name'
            }),
        }


class TaskTypeForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Task Type'
            }),
        }
