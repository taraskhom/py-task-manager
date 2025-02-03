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
                           TaskDeleteView,
                           PositionListView,
                           PositionCreateView,
                           PositionUpdateView,
                           PositionDeleteView,
                           TaskTypeListView,
                           TaskTypeCreateView,
                           TaskTypeUpdateView,
                           TaskTypeDeleteView,
                           WorkerUpdateView)


urlpatterns = [
    #    path('admin/', admin.site.urls),
    path('register/', WorkerRegistrationView.as_view(), name='register'),
    path('login/', WorkerLoginView.as_view(), name='login'),
    path('logout/', worker_logout, name='logout'),
    path('worker/<int:pk>/update/', WorkerUpdateView.as_view(), name='worker_update'),
    path('', index, name='index'),
    path('tasks', TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('task/<int:task_id>/toggle_completion/', change_task_status, name='toggle_task_completion'),
    path('task/create', TaskCreateView.as_view(), name='task_create'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('positions', PositionListView.as_view(), name='positions_list'),
    path('position/create', PositionCreateView.as_view(), name='position_create'),
    path('position/<int:pk>/update', PositionUpdateView.as_view(), name='position_update'),
    path('position/<int:pk>/delete', PositionDeleteView.as_view(), name='position_delete'),
    path('task_types', TaskTypeListView.as_view(), name='task_type_list'),
    path('task_type/create', TaskTypeCreateView.as_view(), name='task_type_create'),
    path('task_type/<int:pk>/update', TaskTypeUpdateView.as_view(), name='task_type_update'),
    path('task_type/<int:pk>/delete', TaskTypeDeleteView.as_view(), name='task_type_delete'),
]

app_name = 'taskhub'
