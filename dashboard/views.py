from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from tasks.models import Task   # import your Task model
from tasks.models import Category

def home(request):
    categories = Category.objects.all()
    return render(request, "dashboard/home.html", {
        "categories": categories
    })

@login_required
def home(request):
    user = request.user
    today = date.today()

    # FIXED: use owner instead of user
    overdue_count = Task.objects.filter(owner=user, due_date__lt=today).count()

    upcoming_count = Task.objects.filter(
        owner=user,
        due_date__gte=today,
        due_date__lte=today + timedelta(days=7)
    ).count()

    total_tasks = Task.objects.filter(owner=user).count()

    context = {
        "overdue_count": overdue_count,
        "upcoming_count": upcoming_count,
        "total_tasks": total_tasks,
    }
    return render(request, "dashboard/home.html", context)
