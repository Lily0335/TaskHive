from django.urls import path
from . import views

app_name = "calendarapp"

urlpatterns = [
    path("", views.calendar_page, name="calendar"),
    path("month/<int:year>/<int:month>/", views.calendar_page, name="calendar_month"),
    path("day/<str:date>/", views.tasks_by_day, name="tasks_by_day"),
    path("create/", views.create_event, name="create_event"),
    path("filter/<str:range>/", views.task_filter, name="task_filter"),
]
