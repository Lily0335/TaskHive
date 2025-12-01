# from django.db import models
# from django.contrib.auth.models import User


# class Category(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     color = models.CharField(max_length=7, default="#000000")

#     def __str__(self):
#         return self.name


# class Task(models.Model):

#     PRIORITY_CHOICES = [
#         ("low", "Low"),
#         ("normal", "Normal"),
#         ("high", "High"),
#     ]

#     REPEAT_CHOICES = [
#         ("none", "No Repeat"),
#         ("daily", "Daily"),
#         ("weekly", "Weekly"),
#         ("monthly", "Monthly"),
#     ]

#     STATUS_CHOICES = [
#         ("pending", "Pending"),
#         ("completed", "Completed"),
#     ]

#     owner = models.ForeignKey(User, on_delete=models.CASCADE)

#     title = models.CharField(max_length=255)
#     description = models.TextField(blank=True)

#     due_date = models.DateField(null=True, blank=True)

#     priority = models.CharField(max_length=20,
#                                 choices=PRIORITY_CHOICES,
#                                 default="normal")

#     status = models.CharField(max_length=20,
#                               choices=STATUS_CHOICES,
#                               default="pending")

#     repeat = models.CharField(max_length=20,
#                               choices=REPEAT_CHOICES,
#                               default="none")

#     category = models.ForeignKey(
#         Category,
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL
#     )

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

PRIORITY = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
]

REPEAT = [
    ('none', 'None'),
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
]

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return self.name


class Task(models.Model):
    # Your tasks module uses "user"
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Your dashboard uses "owner" → so we add and auto-sync it
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="task_owner",
        null=True,
        blank=True
    )

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY, default='medium')
    
    due_date = models.DateTimeField(null=True, blank=True)
    reminder_at = models.DateTimeField(null=True, blank=True)
    
    starred = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    repeat = models.CharField(max_length=20, choices=REPEAT, default='none')

    created_at = models.DateTimeField(auto_now_add=True)

    # ⭐ Auto-sync owner with user (critical!)
    def save(self, *args, **kwargs):
        if not self.owner:
            self.owner = self.user
        super().save(*args, **kwargs)

    def mark_completed(self):
        self.completed = True
        self.save()

        if self.repeat != 'none':
            return Task.objects.create(
                user=self.user,
                owner=self.user,   # auto set owner for repeating tasks
                title=self.title,
                description=self.description,
                category=self.category,
                priority=self.priority,
                starred=self.starred,
                repeat=self.repeat,
                due_date=self.next_due_date(),
            )

    def next_due_date(self):
        if not self.due_date:
            return None
        if self.repeat == 'daily':
            return self.due_date + timedelta(days=1)
        if self.repeat == 'weekly':
            return self.due_date + timedelta(days=7)
        if self.repeat == 'monthly':
            return self.due_date + timedelta(days=30)

    def __str__(self):
        return self.title


class SubTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subtasks")
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Attachment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to="task_files/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
