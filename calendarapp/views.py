from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime, date, timedelta
import calendar

from tasks.models import Task
from .models import CalendarEvent


# ---------------------------
# Build items (task + events)
# ---------------------------
def build_items_map(user):
    items_map = {}

    # ---- TASKS ----
    for t in Task.objects.filter(owner=user):
        if not t.due_date:      # avoid NoneType error
            continue

        key = t.due_date.strftime("%Y-%m-%d")

        items_map.setdefault(key, []).append({
            "type": "task",
            "title": t.title,
            "priority": t.priority,
        })

    # ---- EVENTS ----
    for e in CalendarEvent.objects.filter(owner=user):
        key = e.date.strftime("%Y-%m-%d")

        items_map.setdefault(key, []).append({
            "type": "event",
            "title": e.title,
            "priority": None,
        })

    return items_map



# ---------------------------
# Main calendar page
# ---------------------------
@login_required
def calendar_page(request, year=None, month=None):
    today = date.today()

    # If no year/month -> current
    if year is None or month is None:
        year = today.year
        month = today.month

    year = int(year)
    month = int(month)

    view_date = date(year, month, 1)

    # PREVIOUS month
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year

    # NEXT month
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year

    # Calendar grid
    cal = calendar.Calendar(firstweekday=6)
    calendar_weeks = list(cal.monthdatescalendar(year, month))

    # Items (tasks + events)
    items_map = build_items_map(request.user)

    # ---- FIXED REMINDERS ----
    reminders = Task.objects.filter(
        owner=request.user,
        status="In Progress",                          # correct field
        due_date__isnull=False,                        # avoid None
        due_date__gte=today,                           # due today or later
        due_date__lte=today + timedelta(days=1)        # within next 24 hours
    )

    context = {
        "view_date": view_date,
        "today": today,
        "calendar_weeks": calendar_weeks,
        "items_map": items_map,
        "reminders": reminders,
        "prev_year": prev_year,
        "prev_month": prev_month,
        "next_year": next_year,
        "next_month": next_month,
    }

    return render(request, "calendarapp/calendar.html", context)



# ---------------------------
# Day view
# ---------------------------
@login_required
def tasks_by_day(request, date):
    dt = datetime.strptime(date, "%Y-%m-%d").date()

    tasks = Task.objects.filter(owner=request.user, due_date=dt)
    events = CalendarEvent.objects.filter(owner=request.user, date=dt)

    return render(request, "calendarapp/tasks_by_day.html", {
        "date": dt,
        "tasks": tasks,
        "events": events,
    })



# ---------------------------
# Create Calendar Event
# ---------------------------
@login_required
def create_event(request):
    if request.method == "POST":
        date_str = request.POST.get("date")

        CalendarEvent.objects.create(
            owner=request.user,
            title=request.POST.get("title"),
            note=request.POST.get("note"),
            date=datetime.strptime(date_str, "%Y-%m-%d").date(),
        )
        return redirect("calendarapp:calendar")

    return redirect("calendarapp:calendar")



# ---------------------------
# Filters: Today / Week / Month
# ---------------------------
@login_required
def task_filter(request, range):
    today = date.today()

    if range == "today":
        tasks = Task.objects.filter(owner=request.user, due_date=today)

    elif range == "week":
        tasks = Task.objects.filter(
            owner=request.user,
            due_date__gte=today,
            due_date__lte=today + timedelta(days=7)
        )

    elif range == "month":
        tasks = Task.objects.filter(
            owner=request.user,
            due_date__gte=today,
            due_date__lte=today + timedelta(days=30)
        )

    else:
        tasks = []

    return render(request, "calendarapp/filter_results.html", {
        "range": range.capitalize(),
        "tasks": tasks,
    })
