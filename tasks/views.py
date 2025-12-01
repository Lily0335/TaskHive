from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Task, Category, SubTask
from .forms import TaskForm, SubTaskForm, AttachmentForm


# -------------------------------------------------------------
# MAIN HOME (SMART LIST + CATEGORY LIST + SEARCH + COMPLETED)
# -------------------------------------------------------------
@login_required
def task_home(request):
    tasks = Task.objects.filter(user=request.user, completed=False)
    completed_tasks = Task.objects.filter(user=request.user, completed=True)

    auto = request.GET.get("auto")

    # -----------------------------
    # SMART LIST FIX (SQLite SAFE)
    # -----------------------------
    now = timezone.now()

    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timezone.timedelta(days=1)

    tomorrow_start = today_start + timezone.timedelta(days=1)
    tomorrow_end = today_start + timezone.timedelta(days=2)

    upcoming_end = today_start + timezone.timedelta(days=7)

    if auto == "today":
        tasks = tasks.filter(due_date__gte=today_start, due_date__lt=today_end)

    elif auto == "tomorrow":
        tasks = tasks.filter(due_date__gte=tomorrow_start, due_date__lt=tomorrow_end)

    elif auto == "upcoming":
        tasks = tasks.filter(due_date__gte=today_end, due_date__lt=upcoming_end)

    elif auto == "overdue":
        tasks = tasks.filter(due_date__lt=today_start, completed=False)

    # Search bar
    query = request.GET.get("search", "")
    if query:
        tasks = tasks.filter(title__icontains=query)

    categories = Category.objects.filter(user=request.user)

    return render(request, "tasks/tasks.html", {
        "tasks": tasks,
        "completed_tasks": completed_tasks,
        "categories": categories,
    })


# -------------------------------------------------------------
# ADD TASK (Category Name + Color + Subtasks)
# -------------------------------------------------------------
@login_required
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST, user=request.user)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user

            # ⭐ Category Logic
            cat_name = form.cleaned_data.get("category_name")
            cat_color = form.cleaned_data.get("category_color") or "#000000"

            if cat_name:
                category, created = Category.objects.get_or_create(
                    user=request.user,
                    name=cat_name,
                    defaults={"color": cat_color},
                )
                task.category = category

            task.save()

            # Subtasks
            for st in request.POST.getlist("subtask"):
                if st.strip():
                    SubTask.objects.create(task=task, title=st)

            return redirect("tasks:home")

    else:
        form = TaskForm(user=request.user)

    categories = Category.objects.filter(user=request.user)

    return render(request, "tasks/task_form.html", {
        "form": form,
        "categories": categories,
    })


# -------------------------------------------------------------
# EDIT TASK
# -------------------------------------------------------------
@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("tasks:home")
    else:
        form = TaskForm(instance=task, user=request.user)

    return render(request, "tasks/task_form.html", {
        "form": form,
        "task": task,
        "edit_mode": True,
    })


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == "POST":
        task.delete()
        return redirect("tasks:home")  # ✔ correct redirect (task_list exist nahi karta)

    return render(request, "tasks/delete_confirm.html", {"task": task})



# -------------------------------------------------------------
# TASK LIST (for edit/delete view)
# -------------------------------------------------------------
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, "tasks/task_list.html", {"tasks": tasks})


# -------------------------------------------------------------
# TASK DETAIL VIEW
# -------------------------------------------------------------
@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    sub_form = SubTaskForm()
    attach_form = AttachmentForm()

    return render(request, "tasks/task_detail.html", {
        "task": task,
        "sub_form": sub_form,
        "attach_form": attach_form,
    })


# -------------------------------------------------------------
# COMPLETE / STAR
# -------------------------------------------------------------
@login_required
def complete_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    task.mark_completed()
    return redirect("tasks:home")


@login_required
def toggle_star(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    task.starred = not task.starred
    task.save()
    return redirect("tasks:home")


# -------------------------------------------------------------
# CATEGORY FILTER PAGE
# -------------------------------------------------------------
@login_required
def tasks_by_category(request, pk):
    category = get_object_or_404(Category, id=pk, user=request.user)

    tasks = Task.objects.filter(user=request.user, category=category, completed=False)
    completed_tasks = Task.objects.filter(user=request.user, category=category, completed=True)
    categories = Category.objects.filter(user=request.user)

    return render(request, "tasks/tasks.html", {
        "tasks": tasks,
        "completed_tasks": completed_tasks,
        "categories": categories,
        "selected_category": category,
    })
