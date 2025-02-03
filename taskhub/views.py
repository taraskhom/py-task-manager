from urllib.parse import urlencode

from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.views import generic
from .forms import WorkerRegistrationForm
from .models import Worker, Task


def index(request):
    return render(request, 'taskhub/index.html', {})


class WorkerRegistrationView(generic.CreateView):
    model = Worker
    form_class = WorkerRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('taskhub:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class WorkerLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('taskhub:index')


def worker_logout(request):
    if request.method == 'GET':
        logout(request)
        return redirect('taskhub:index')


class TaskListView(generic.ListView):
    model = Task
    template_name = 'taskhub/task_list.html'
    paginate_by = 6
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
        ).order_by('deadline', '-priority')

        context['completed_tasks'] = Task.objects.filter(
            is_completed=True, assignees=self.request.user
        ).order_by('-deadline')

        context['assigned_tasks'] = Task.objects.filter(
            assigned_by=self.request.user
        ).order_by('-deadline')

        return context


class TaskDetailView(generic.DetailView):
    model = Task
    template_name = 'taskhub/task_detail.html'


def change_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_completed = not task.is_completed
    task.save()

    next_url = request.GET.get('next')
    if next_url:
        return HttpResponseRedirect(next_url)

    return redirect('taskhub:task_detail', pk=task.id)


class TaskCreateView(generic.CreateView):
    model = Task
    template_name = 'taskhub/task_form.html'
    fields = ['name', 'description', 'deadline', 'priority', 'task_type', 'assignees']

    def form_valid(self, form):
        form.instance.assigned_by = self.request.user
        self.object = form.save()
        return redirect(reverse_lazy('taskhub:task_list') + '?status=assigned')


class TaskUpdateView(generic.UpdateView):
    model = Task
    template_name = 'taskhub/task_form.html'
    fields = ['name', 'description', 'deadline', 'priority', 'task_type', 'assignees']

    def form_valid(self, form):
        form.instance.assigned_by = self.request.user
        self.object = form.save()
        return redirect(reverse_lazy('taskhub:task_list') + '?status=assigned')


class TaskDeleteView(generic.DeleteView):
    model = Task
    template_name = None

    def get_success_url(self):
        url = reverse_lazy('taskhub:task_list')
        query_params = urlencode({'status': 'assigned'})
        return f"{url}?{query_params}"
