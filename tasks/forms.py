from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'status']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'border rounded px-2 py-1 w-full'}),
            'priority': forms.Select(attrs={'class': 'border rounded px-2 py-1 w-full'}),
            'status': forms.Select(attrs={'class': 'border rounded px-2 py-1 w-full'}),
            'title': forms.TextInput(attrs={'class': 'border rounded px-2 py-1 w-full'}),
            'description': forms.Textarea(attrs={'class': 'border rounded px-2 py-1 w-full', 'rows': 3}),
        }
