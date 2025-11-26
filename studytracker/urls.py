from django.urls import path
from . import views

app_name = "studytracker"

urlpatterns = [
    path("", views.study_list, name="list"),
    path("add/", views.study_create, name="add"),
    path("edit/<int:pk>/", views.study_update, name="edit"),
    path("delete/<int:pk>/", views.study_delete, name="delete"),
]
