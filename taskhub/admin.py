from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Position, Worker, TaskType, Task


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Worker)
class WorkerAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('position',)}),
    )
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'position',
        'is_staff'
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'deadline',
        'is_completed',
        'priority',
        'task_type',
        'assigned_by'
    )
    list_filter = ('is_completed', 'priority', 'task_type', 'deadline')
    search_fields = ('name', 'description')
    filter_horizontal = ('assignees',)
