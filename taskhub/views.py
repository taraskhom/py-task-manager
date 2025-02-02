from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.views import generic
from .forms import WorkerRegistrationForm
from .models import Worker


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
