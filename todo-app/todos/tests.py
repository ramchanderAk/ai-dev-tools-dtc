from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import date, timedelta
from .models import Todo
from .forms import TodoForm


# ============================================
# MODEL TESTS
# ============================================

class TodoModelTest(TestCase):
    """Test cases for Todo model"""

    def setUp(self):
        """Set up test data"""
        self.todo = Todo.objects.create(
            title='Test TODO',
            description='Test description',
            due_date=date.today() + timedelta(days=7),
            priority='high'
        )

    def test_todo_creation(self):
        """Test creating a TODO with all fields"""
        self.assertEqual(self.todo.title, 'Test TODO')
        self.assertEqual(self.todo.description, 'Test description')
        self.assertEqual(self.todo.priority, 'high')
        self.assertFalse(self.todo.is_resolved)

    def test_todo_default_values(self):
        """Test default values for optional fields"""
        todo = Todo.objects.create(title='Minimal TODO')
        self.assertEqual(todo.priority, 'medium')
        self.assertFalse(todo.is_resolved)
        self.assertIsNone(todo.description)
        self.assertIsNone(todo.due_date)

    def test_str_method(self):
        """Test string representation"""
        self.assertEqual(str(self.todo), 'Test TODO')

    def test_is_overdue_future_date(self):
        """Test is_overdue returns False for future dates"""
        self.assertFalse(self.todo.is_overdue())

    def test_is_overdue_past_date(self):
        """Test is_overdue returns True for past dates"""
        self.todo.due_date = date.today() - timedelta(days=1)
        self.todo.save()
        self.assertTrue(self.todo.is_overdue())

    def test_is_overdue_resolved_todo(self):
        """Test is_overdue returns False for resolved TODOs"""
        self.todo.due_date = date.today() - timedelta(days=1)
        self.todo.is_resolved = True
        self.todo.save()
        self.assertFalse(self.todo.is_overdue())

    def test_is_overdue_no_due_date(self):
        """Test is_overdue returns False when no due date"""
        self.todo.due_date = None
        self.todo.save()
        self.assertFalse(self.todo.is_overdue())

    def test_get_absolute_url(self):
        """Test get_absolute_url returns correct URL"""
        url = self.todo.get_absolute_url()
        self.assertEqual(url, f'/todo/{self.todo.pk}/')

    def test_auto_timestamps(self):
        """Test that timestamps are automatically set"""
        self.assertIsNotNone(self.todo.created_at)
        self.assertIsNotNone(self.todo.updated_at)

    def test_ordering(self):
        """Test default ordering"""
        todo1 = Todo.objects.create(title='Active High', priority='high', is_resolved=False)
        todo2 = Todo.objects.create(title='Completed High', priority='high', is_resolved=True)
        todo3 = Todo.objects.create(title='Active Low', priority='low', is_resolved=False)

        todos = Todo.objects.all()
        # Active todos should come before completed
        self.assertEqual(todos[0].is_resolved, False)


# ============================================
# VIEW TESTS
# ============================================

class TodoListViewTest(TestCase):
    """Test cases for Todo list view"""

    def setUp(self):
        self.client = Client()
        self.url = reverse('todo-list')
        # Create test data
        Todo.objects.create(title='Active TODO', is_resolved=False)
        Todo.objects.create(title='Completed TODO', is_resolved=True)

    def test_list_view_get(self):
        """Test GET request to list view"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_list.html')
        self.assertIn('todos', response.context)

    def test_list_view_shows_all_todos(self):
        """Test list view displays all TODOs"""
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['todos']), 2)

    def test_filter_active_todos(self):
        """Test filtering active TODOs"""
        response = self.client.get(self.url + '?filter=active')
        self.assertEqual(len(response.context['todos']), 1)
        self.assertFalse(response.context['todos'][0].is_resolved)

    def test_filter_completed_todos(self):
        """Test filtering completed TODOs"""
        response = self.client.get(self.url + '?filter=completed')
        self.assertEqual(len(response.context['todos']), 1)
        self.assertTrue(response.context['todos'][0].is_resolved)

    def test_statistics_in_context(self):
        """Test statistics are correctly calculated"""
        response = self.client.get(self.url)
        self.assertEqual(response.context['total_count'], 2)
        self.assertEqual(response.context['active_count'], 1)
        self.assertEqual(response.context['completed_count'], 1)


class TodoDetailViewTest(TestCase):
    """Test cases for Todo detail view"""

    def setUp(self):
        self.client = Client()
        self.todo = Todo.objects.create(title='Detail Test TODO')
        self.url = reverse('todo-detail', args=[self.todo.pk])

    def test_detail_view_get(self):
        """Test GET request to detail view"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_detail.html')
        self.assertEqual(response.context['todo'], self.todo)

    def test_detail_view_nonexistent_todo(self):
        """Test detail view with non-existent TODO returns 404"""
        url = reverse('todo-detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TodoCreateViewTest(TestCase):
    """Test cases for Todo create view"""

    def setUp(self):
        self.client = Client()
        self.url = reverse('todo-create')

    def test_create_view_get(self):
        """Test GET request shows create form"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_form.html')

    def test_create_todo_valid_data(self):
        """Test creating TODO with valid data"""
        data = {
            'title': 'New TODO',
            'description': 'New description',
            'priority': 'high',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(Todo.objects.count(), 1)
        self.assertRedirects(response, reverse('todo-list'))

        todo = Todo.objects.first()
        self.assertEqual(todo.title, 'New TODO')
        self.assertEqual(todo.priority, 'high')

    def test_create_todo_invalid_data(self):
        """Test creating TODO with invalid data"""
        initial_count = Todo.objects.count()
        data = {'title': ''}  # Empty title
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Todo.objects.count(), initial_count)
        self.assertContains(response, 'This field is required')

    def test_create_todo_with_due_date(self):
        """Test creating TODO with due date"""
        data = {
            'title': 'TODO with date',
            'due_date': date.today() + timedelta(days=5),
            'priority': 'medium',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(Todo.objects.count(), 1)
        todo = Todo.objects.first()
        self.assertIsNotNone(todo.due_date)


class TodoUpdateViewTest(TestCase):
    """Test cases for Todo update view"""

    def setUp(self):
        self.client = Client()
        self.todo = Todo.objects.create(
            title='Original Title',
            priority='low'
        )
        self.url = reverse('todo-update', args=[self.todo.pk])

    def test_update_view_get(self):
        """Test GET request shows update form with data"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_form.html')
        self.assertContains(response, 'Original Title')

    def test_update_todo_valid_data(self):
        """Test updating TODO with valid data"""
        data = {
            'title': 'Updated Title',
            'description': 'Updated description',
            'priority': 'high',
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('todo-list'))

        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated Title')
        self.assertEqual(self.todo.priority, 'high')

    def test_update_todo_invalid_data(self):
        """Test updating TODO with invalid data"""
        data = {'title': '', 'priority': 'high'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)

        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Original Title')


class TodoDeleteViewTest(TestCase):
    """Test cases for Todo delete view"""

    def setUp(self):
        self.client = Client()
        self.todo = Todo.objects.create(title='To Delete')
        self.url = reverse('todo-delete', args=[self.todo.pk])

    def test_delete_view_get(self):
        """Test GET request shows confirmation page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_confirm_delete.html')
        self.assertContains(response, 'To Delete')

    def test_delete_todo_post(self):
        """Test POST request deletes TODO"""
        initial_count = Todo.objects.count()
        response = self.client.post(self.url)
        self.assertEqual(Todo.objects.count(), initial_count - 1)
        self.assertRedirects(response, reverse('todo-list'))
        self.assertFalse(Todo.objects.filter(pk=self.todo.pk).exists())


class TodoToggleViewTest(TestCase):
    """Test cases for toggling TODO status"""

    def setUp(self):
        self.client = Client()
        self.todo = Todo.objects.create(title='Toggle Test', is_resolved=False)
        self.url = reverse('todo-toggle', args=[self.todo.pk])

    def test_toggle_from_active_to_completed(self):
        """Test toggling TODO from active to completed"""
        response = self.client.get(self.url)
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.is_resolved)
        self.assertRedirects(response, reverse('todo-list'))

    def test_toggle_from_completed_to_active(self):
        """Test toggling TODO from completed to active"""
        self.todo.is_resolved = True
        self.todo.save()

        response = self.client.get(self.url)
        self.todo.refresh_from_db()
        self.assertFalse(self.todo.is_resolved)
        self.assertRedirects(response, reverse('todo-list'))


# ============================================
# FORM TESTS
# ============================================

class TodoFormTest(TestCase):
    """Test cases for Todo form"""

    def test_form_valid_with_all_fields(self):
        """Test form is valid with all fields"""
        form_data = {
            'title': 'Test TODO',
            'description': 'Test description',
            'due_date': date.today() + timedelta(days=7),
            'priority': 'high',
            'is_resolved': False,
        }
        form = TodoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_valid_with_required_only(self):
        """Test form is valid with only required fields"""
        form_data = {
            'title': 'Minimal TODO',
            'priority': 'medium',
        }
        form = TodoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_without_title(self):
        """Test form is invalid without title"""
        form_data = {
            'description': 'No title',
            'priority': 'low',
        }
        form = TodoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_form_invalid_with_past_due_date(self):
        """Test form is invalid with past due date for new TODO"""
        form_data = {
            'title': 'Past Due',
            'due_date': date.today() - timedelta(days=1),
            'priority': 'medium',
        }
        form = TodoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('due_date', form.errors)

    def test_form_valid_today_due_date(self):
        """Test form is valid with today's due date"""
        form_data = {
            'title': 'Due Today',
            'due_date': date.today(),
            'priority': 'medium',
        }
        form = TodoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_widgets_have_correct_classes(self):
        """Test form widgets have correct CSS classes"""
        form = TodoForm()
        self.assertIn('form-input', form.fields['title'].widget.attrs['class'])
        self.assertIn('form-textarea', form.fields['description'].widget.attrs['class'])


# ============================================
# URL TESTS
# ============================================

class TodoURLTest(TestCase):
    """Test cases for URL routing"""

    def test_list_url_resolves(self):
        """Test list URL resolves correctly"""
        url = reverse('todo-list')
        self.assertEqual(url, '/')

    def test_create_url_resolves(self):
        """Test create URL resolves correctly"""
        url = reverse('todo-create')
        self.assertEqual(url, '/create/')

    def test_detail_url_resolves(self):
        """Test detail URL resolves correctly"""
        url = reverse('todo-detail', args=[1])
        self.assertEqual(url, '/todo/1/')

    def test_update_url_resolves(self):
        """Test update URL resolves correctly"""
        url = reverse('todo-update', args=[1])
        self.assertEqual(url, '/todo/1/edit/')

    def test_delete_url_resolves(self):
        """Test delete URL resolves correctly"""
        url = reverse('todo-delete', args=[1])
        self.assertEqual(url, '/todo/1/delete/')

    def test_toggle_url_resolves(self):
        """Test toggle URL resolves correctly"""
        url = reverse('todo-toggle', args=[1])
        self.assertEqual(url, '/todo/1/toggle/')


# ============================================
# INTEGRATION TESTS
# ============================================

class TodoIntegrationTest(TestCase):
    """Integration tests for complete workflows"""

    def setUp(self):
        self.client = Client()

    def test_complete_crud_workflow(self):
        """Test complete Create → Read → Update → Delete workflow"""
        # CREATE
        create_data = {
            'title': 'Integration Test TODO',
            'description': 'Full workflow test',
            'priority': 'high',
        }
        create_response = self.client.post(reverse('todo-create'), create_data)
        self.assertEqual(Todo.objects.count(), 1)
        todo = Todo.objects.first()

        # READ (List)
        list_response = self.client.get(reverse('todo-list'))
        self.assertContains(list_response, 'Integration Test TODO')

        # READ (Detail)
        detail_response = self.client.get(reverse('todo-detail', args=[todo.pk]))
        self.assertContains(detail_response, 'Integration Test TODO')

        # UPDATE
        update_data = {
            'title': 'Updated Integration TODO',
            'description': 'Updated description',
            'priority': 'low',
        }
        update_response = self.client.post(
            reverse('todo-update', args=[todo.pk]),
            update_data
        )
        todo.refresh_from_db()
        self.assertEqual(todo.title, 'Updated Integration TODO')

        # DELETE
        delete_response = self.client.post(reverse('todo-delete', args=[todo.pk]))
        self.assertEqual(Todo.objects.count(), 0)

    def test_toggle_and_filter_workflow(self):
        """Test creating, toggling, and filtering TODOs"""
        # Create active TODO
        todo1 = Todo.objects.create(title='Active TODO', is_resolved=False)
        todo2 = Todo.objects.create(title='Another Active', is_resolved=False)

        # Toggle one to completed
        self.client.get(reverse('todo-toggle', args=[todo1.pk]))

        # Check active filter
        active_response = self.client.get(reverse('todo-list') + '?filter=active')
        self.assertEqual(len(active_response.context['todos']), 1)

        # Check completed filter
        completed_response = self.client.get(reverse('todo-list') + '?filter=completed')
        self.assertEqual(len(completed_response.context['todos']), 1)

    def test_overdue_detection_workflow(self):
        """Test overdue TODO detection"""
        # Create overdue TODO
        overdue_todo = Todo.objects.create(
            title='Overdue TODO',
            due_date=date.today() - timedelta(days=1),
            is_resolved=False
        )

        # Check it's detected as overdue
        self.assertTrue(overdue_todo.is_overdue())

        # Mark as resolved
        overdue_todo.is_resolved = True
        overdue_todo.save()

        # Check it's no longer overdue
        self.assertFalse(overdue_todo.is_overdue())
