from django.db import models
from django.contrib.auth.models import User

class StickyNote(models.Model):
    COLOR_CHOICES = [
        ("yellow", "Yellow"),
        ("red", "Red"),
        ("blue", "Blue"),
        ("green", "Green"),
        ("purple", "Purple"),
        ("gray", "Gray"),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default="yellow")
    pinned = models.BooleanField(default=False)
    x = models.IntegerField(default=100)
    y = models.IntegerField(default=100)
    width = models.IntegerField(default=250)
    height = models.IntegerField(default=250)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
