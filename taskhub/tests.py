from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from taskhub.models import Task, Position, TaskType


Worker = get_user_model()


class WorkerRegistrationViewTests(TestCase):
    def test_registration_creates_user_and_logs_in(self):
        registration_url = reverse('taskhub:register')
        position = Position.objects.create(name="Test Position")
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'position': position.pk,
        }
        response = self.client.post(registration_url, data, follow=True)
        if response.context and 'form' in response.context:
            print("Form errors:", response.context['form'].errors)
        self.assertTrue(Worker.objects.filter(username='newuser').exists())
        self.assertTrue(response.context['user'].is_authenticated)
        index_url = reverse('taskhub:index')
        self.assertRedirects(response, index_url)


class WorkerLogoutViewTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Test Position")
        self.user = Worker.objects.create_user(
            username='testuser',
            password='password123',
            position=self.position
        )

    def test_logout_get_request_logs_out(self):
        self.client.login(username='testuser', password='password123')
        logout_url = reverse('taskhub:logout')
        response = self.client.get(logout_url, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
        index_url = reverse('taskhub:index')
        self.assertRedirects(response, index_url)


class TaskListViewTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Test Position")
        self.user = Worker.objects.create_user(
            username='testuser',
            password='password123',
            position=self.position
        )
        self.client.force_login(self.user)
        self.task_type = TaskType.objects.create(name="Default Type")
        self.task_uncompleted = Task.objects.create(
            name='Uncompleted Task',
            deadline=timezone.now() + timedelta(days=1),
            is_completed=False,
            assigned_by=self.user,
            priority=1,
            task_type=self.task_type,
        )
        self.task_uncompleted.assignees.add(self.user)

        self.task_completed = Task.objects.create(
            name='Completed Task',
            deadline=timezone.now() + timedelta(days=2),
            is_completed=True,
            assigned_by=self.user,
            priority=2,
            task_type=self.task_type,
        )
        self.task_completed.assignees.add(self.user)

        self.task_assigned = Task.objects.create(
            name='Assigned Task',
            deadline=timezone.now() + timedelta(days=3),
            is_completed=False,
            assigned_by=self.user,
            priority=3,
            task_type=self.task_type,
        )

        self.other_position = Position.objects.create(name="Other Position")
        self.other_user = Worker.objects.create_user(
            username='other',
            password='password123',
            position=self.other_position
        )
        self.task_other = Task.objects.create(
            name='Other Task',
            deadline=timezone.now() + timedelta(days=4),
            is_completed=False,
            assigned_by=self.other_user,
            priority=1,
            task_type=self.task_type,
        )
        self.task_other.assignees.add(self.other_user)

    def test_get_queryset_filters_tasks_by_assignee(self):
        url = reverse('taskhub:task_list')
        response = self.client.get(url)
        tasks = response.context['tasks']
        self.assertIn(self.task_uncompleted, tasks)
        self.assertIn(self.task_completed, tasks)
        self.assertNotIn(self.task_assigned, tasks)
        self.assertNotIn(self.task_other, tasks)

    def test_context_data_contains_correct_task_lists(self):
        url = reverse('taskhub:task_list')
        response = self.client.get(url + '?status=some_status')
        context = response.context
        self.assertEqual(context.get('status'), 'some_status')

        uncompleted_tasks = context.get('uncompleted_tasks')
        self.assertIn(self.task_uncompleted, uncompleted_tasks)
        self.assertNotIn(self.task_completed, uncompleted_tasks)

        completed_tasks = context.get('completed_tasks')
        self.assertIn(self.task_completed, completed_tasks)
        self.assertNotIn(self.task_uncompleted, completed_tasks)

        assigned_tasks = context.get('assigned_tasks')
        self.assertIn(self.task_uncompleted, assigned_tasks)
        self.assertIn(self.task_completed, assigned_tasks)
        self.assertIn(self.task_assigned, assigned_tasks)
        self.assertNotIn(self.task_other, assigned_tasks)


class ChangeTaskStatusViewTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Test Position")
        self.user = Worker.objects.create_user(
            username='testuser',
            password='password123',
            position=self.position
        )
        self.client.force_login(self.user)
        self.task_type = TaskType.objects.create(name="Default Type")
        self.task = Task.objects.create(
            name='Toggle Task',
            deadline=timezone.now() + timedelta(days=1),
            is_completed=False,
            assigned_by=self.user,
            priority=1,
            task_type=self.task_type,
        )
        self.task.assignees.add(self.user)

    def test_toggle_task_status_without_next(self):
        toggle_url = reverse('taskhub:toggle_task_completion', kwargs={'task_id': self.task.id})
        response = self.client.get(toggle_url)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)
        expected_redirect = reverse('taskhub:task_detail', kwargs={'pk': self.task.id})
        self.assertRedirects(response, expected_redirect)

    def test_toggle_task_status_with_next(self):
        next_url = reverse('taskhub:task_list')
        toggle_url = reverse('taskhub:toggle_task_completion', kwargs={'task_id': self.task.id})
        response = self.client.get(f"{toggle_url}?next={next_url}")
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)
        self.assertRedirects(response, next_url)


class TaskCreateViewTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Test Position")
        self.user = Worker.objects.create_user(
            username='testuser',
            password='password123',
            position=self.position
        )
        self.client.force_login(self.user)
        self.task_type = TaskType.objects.create(name="Bug")

    def test_task_creation_sets_assigned_by_and_redirects(self):
        create_url = reverse('taskhub:task_create')
        deadline = (timezone.now() + timedelta(days=5)).strftime("%Y-%m-%d")
        data = {
            'name': 'New Task',
            'description': 'Task description goes here.',
            'deadline': deadline,
            'priority': 2,
            'task_type': self.task_type.pk,
            'assignees': [self.user.pk],
        }
        response = self.client.post(create_url, data)
        task = Task.objects.get(name='New Task')
        self.assertEqual(task.assigned_by, self.user)
        expected_redirect = reverse('taskhub:task_list') + '?status=assigned'
        self.assertRedirects(response, expected_redirect)
