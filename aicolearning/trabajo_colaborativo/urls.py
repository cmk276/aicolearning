from django.urls import path

from . import views

app_name = "trabajo_colaborativo"
urlpatterns = [
    path("", views.index, name="index"),
]