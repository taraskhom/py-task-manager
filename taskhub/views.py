from urllib.parse import urlencode
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.views import generic

from taskhub.forms import (
    WorkerRegistrationForm,
    WorkerUpdateForm,
    TaskForm,
    TaskTypeForm,
    PositionForm
)
from taskhub.models import Worker, Task, Position, TaskType


def index(request):
    return render(request, 'taskhub/index.html', {})


class WorkerRegistrationView(generic.CreateView):
    model = Worker
    form_class = WorkerRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('taskhub:index')

    def form_valid(self, form):
        self.object = form.save()
        self.object.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())


class WorkerLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('taskhub:index')


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    template_name = 'registration/profile_page.html'
    success_url = reverse_lazy('taskhub:task_list')


@login_required
def worker_logout(request):
    if request.method == 'GET':
        logout(request)
        return redirect('taskhub:index')


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = 'taskhub/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = Task.objects.filter(assignees=self.request.user)

        return queryset

    def get_context_data(
        self, **kwargs
    ):
        context = super().get_context_data(**kwargs)

        context['status'] = self.request.GET.get('status', None)

        context['uncompleted_tasks'] = Task.objects.filter(
            is_completed=False, assignees=self.request.user
        ).order_by('deadline', 'priority')

        context['completed_tasks'] = Task.objects.filter(
            is_completed=True, assignees=self.request.user
        ).order_by('-deadline')

        context['assigned_tasks'] = Task.objects.filter(
            assigned_by=self.request.user
        ).order_by('-deadline')

        return context


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = 'taskhub/task_detail.html'


@login_required
def change_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_completed = not task.is_completed
    task.save()

    next_url = request.GET.get('next')
    if next_url:
        return HttpResponseRedirect(next_url)

    return redirect('taskhub:task_detail', pk=task.id)


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'taskhub/task_form.html'

    def form_valid(self, form):
        form.instance.assigned_by = self.request.user
        self.object = form.save()
        return redirect(reverse_lazy('taskhub:task_list') + '?status=assigned')


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    template_name = 'taskhub/task_form.html'
    form_class = TaskForm

    def form_valid(self, form):
        form.instance.assigned_by = self.request.user
        self.object = form.save()
        return redirect(reverse_lazy('taskhub:task_list') + '?status=assigned')


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = None

    def get_success_url(self):
        url = reverse_lazy('taskhub:task_list')
        query_params = urlencode({'status': 'assigned'})
        return f"{url}?{query_params}"


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    template_name = 'taskhub/position_list.html'
    context_object_name = 'positions'


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    template_name = 'taskhub/position_form.html'
    form_class = PositionForm
    success_url = reverse_lazy('taskhub:positions_list')


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    template_name = 'taskhub/position_form.html'
    form_class = PositionForm
    success_url = reverse_lazy('taskhub:positions_list')


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    template_name = 'taskhub/position_confirm_delete.html'
    success_url = reverse_lazy('taskhub:positions_list')


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = 'taskhub/task_type_list.html'
    context_object_name = 'task_types'


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    template_name = 'taskhub/task_type_form.html'
    form_class = TaskTypeForm
    success_url = reverse_lazy('taskhub:task_type_list')


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    template_name = 'taskhub/task_type_form.html'
    form_class = TaskTypeForm
    success_url = reverse_lazy('taskhub:task_type_list')


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = 'taskhub/task_type_confirm_delete.html'
    success_url = reverse_lazy('taskhub:task_type_list')
