from django.urls import path

from taskhub.views import (WorkerRegistrationView,
                           WorkerLoginView,
                           index,
                           worker_logout,
                           TaskListView,
                           TaskCreateView,
                           change_task_status,
                           TaskDetailView,
                           TaskUpdateView,
                           TaskDeleteView)


urlpatterns = [
    #    path('admin/', admin.site.urls),
    path('register/', WorkerRegistrationView.as_view(), name='register'),
    path('login/', WorkerLoginView.as_view(), name='login'),
    path('logout/', worker_logout, name='logout'),
    path('', index, name='index'),
    path('task_list', TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('task/<int:task_id>/toggle_completion/', change_task_status, name='toggle_task_completion'),
    path('task_create', TaskCreateView.as_view(), name='task_create'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
]

app_name = 'taskhub'
