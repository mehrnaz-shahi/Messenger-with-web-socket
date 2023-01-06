from django.urls import path

from . import views


app_name = "group"

urlpatterns = [
    path('<int:group_id>/', views.group_view, name="group"),
]