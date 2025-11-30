from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Todo
from .forms import TodoForm


class TodoListView(ListView):
    """View to display list of all TODOs."""
    model = Todo
    template_name = 'todos/todo_list.html'
    context_object_name = 'todos'
    paginate_by = 20

    def get_queryset(self):
        """Filter todos based on query parameters."""
        queryset = super().get_queryset()
        filter_type = self.request.GET.get('filter', 'all')

        if filter_type == 'active':
            queryset = queryset.filter(is_resolved=False)
        elif filter_type == 'completed':
            queryset = queryset.filter(is_resolved=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_type'] = self.request.GET.get('filter', 'all')

        # Count statistics
        context['total_count'] = Todo.objects.count()
        context['active_count'] = Todo.objects.filter(is_resolved=False).count()
        context['completed_count'] = Todo.objects.filter(is_resolved=True).count()

        return context


class TodoDetailView(DetailView):
    """View to display a single TODO."""
    model = Todo
    template_name = 'todos/todo_detail.html'
    context_object_name = 'todo'


class TodoCreateView(CreateView):
    """View to create a new TODO."""
    model = Todo
    form_class = TodoForm
    template_name = 'todos/todo_form.html'
    success_url = reverse_lazy('todo-list')

    def form_valid(self, form):
        messages.success(self.request, 'TODO created successfully!')
        return super().form_valid(form)


class TodoUpdateView(UpdateView):
    """View to update an existing TODO."""
    model = Todo
    form_class = TodoForm
    template_name = 'todos/todo_form.html'
    success_url = reverse_lazy('todo-list')

    def form_valid(self, form):
        messages.success(self.request, 'TODO updated successfully!')
        return super().form_valid(form)


class TodoDeleteView(DeleteView):
    """View to delete a TODO."""
    model = Todo
    template_name = 'todos/todo_confirm_delete.html'
    success_url = reverse_lazy('todo-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'TODO deleted successfully!')
        return super().delete(request, *args, **kwargs)


def toggle_todo(request, pk):
    """Toggle the resolved status of a TODO."""
    todo = get_object_or_404(Todo, pk=pk)
    todo.is_resolved = not todo.is_resolved
    todo.save()

    status = "completed" if todo.is_resolved else "reopened"
    messages.success(request, f'TODO marked as {status}!')

    return redirect('todo-list')
