from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views.generic.edit import CreateView
from .forms import WorkerRegistrationForm
from .models import Worker


def index(request):
    return render(request, 'taskhub/index.html', {})


class WorkerRegistrationView(CreateView):
    model = Worker
    form_class = WorkerRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('taskhub:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
