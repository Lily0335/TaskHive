from django import forms
from .models import Task, SubTask, Category, Attachment

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "priority",
            "due_date",
            "reminder_at",
            "repeat",
        ]

        widgets = {
            "title": forms.TextInput(),
            "description": forms.Textarea(),
            "priority": forms.Select(),
            "repeat": forms.Select(),
            "due_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "reminder_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)


class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ["title"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "color"]


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ["file"]
