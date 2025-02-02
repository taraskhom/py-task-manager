from django.urls import path

from taskhub.views import WorkerRegistrationView, WorkerLoginView, index, worker_logout


urlpatterns = [
    #    path('admin/', admin.site.urls),
    path('register/', WorkerRegistrationView.as_view(), name='register'),
    path('login/', WorkerLoginView.as_view(), name='login'),
    path('logout/', worker_logout, name='logout'),
    path('', index, name='index')
]

app_name = "taskhub"
