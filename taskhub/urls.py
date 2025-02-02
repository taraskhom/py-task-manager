from django.urls import path

from taskhub.views import WorkerRegistrationView, index


urlpatterns = [
    #    path('admin/', admin.site.urls),
    path('register', WorkerRegistrationView.as_view(), name='register'),
    path('', index, name='index')
]

app_name = "taskhub"
