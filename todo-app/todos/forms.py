from django import forms
from django.utils import timezone
from .models import Todo


class TodoForm(forms.ModelForm):
    """Form for creating and updating TODO items."""

    class Meta:
        model = Todo
        fields = ['title', 'description', 'due_date', 'priority', 'is_resolved']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter TODO title...',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Add a description (optional)...',
                'rows': 4,
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select',
            }),
            'is_resolved': forms.CheckboxInput(attrs={
                'class': 'form-checkbox',
            }),
        }

    def clean_due_date(self):
        """Validate that due date is not in the past for new TODOs."""
        due_date = self.cleaned_data.get('due_date')

        # Only validate for new TODOs or when due date is being changed
        if due_date and not self.instance.pk:
            if due_date < timezone.now().date():
                raise forms.ValidationError("Due date cannot be in the past.")

        return due_date


