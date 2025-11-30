from django.db import models
from django.utils import timezone
from django.urls import reverse


class Todo(models.Model):
    """Model representing a TODO item."""

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=200, help_text='Enter the TODO title')
    description = models.TextField(blank=True, null=True, help_text='Optional detailed description')
    due_date = models.DateField(blank=True, null=True, help_text='Optional due date')
    is_resolved = models.BooleanField(default=False, help_text='Mark as complete')
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        help_text='Priority level'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['is_resolved', '-priority', 'due_date', '-created_at']
        verbose_name = 'TODO'
        verbose_name_plural = 'TODOs'

    def __str__(self):
        return self.title

    def is_overdue(self):
        """Check if the TODO is overdue (past due date and not resolved)."""
        if self.due_date and not self.is_resolved:
            return timezone.now().date() > self.due_date
        return False

    def get_absolute_url(self):
        """Returns the URL to access a particular TODO instance."""
        return reverse('todo-detail', args=[str(self.id)])
