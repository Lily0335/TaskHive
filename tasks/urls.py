# from django.urls import path
# from . import views

# app_name = "tasks"

# urlpatterns = [
#     path("", views.task_list, name="task_list"),
#     path("create/", views.create_task, name="create_task"),
#     path("<int:task_id>/edit/", views.edit_task, name="edit_task"),
#     path("<int:task_id>/delete/", views.delete_task, name="delete_task"),
#     path("toggle-status/", views.toggle_status, name="toggle_status"),
# ]
from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path("list/", views.task_home, name="home"),

    path("add/", views.add_task, name="add"),

    path("edit/<int:pk>/", views.edit_task, name="edit_task"),

    path("delete/<int:pk>/", views.delete_task, name="delete_task"),

    path("complete/<int:pk>/", views.complete_task, name="complete"),

    path("star/<int:pk>/", views.toggle_star, name="star"),

    path("detail/<int:pk>/", views.task_detail, name="detail"),

    path("category/<int:pk>/", views.tasks_by_category, name="tasks_by_category"),
]
