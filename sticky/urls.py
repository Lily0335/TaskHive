from django.urls import path
from . import views

app_name = "sticky"

urlpatterns = [
    path("", views.sticky_wall, name="wall"),

    path("create/", views.create_note, name="create"),
    path("edit/<int:pk>/", views.edit_note, name="edit"),
    path("delete/<int:pk>/", views.delete_note, name="delete"),
    path("pin/<int:pk>/", views.pin_note, name="pin"),
]
