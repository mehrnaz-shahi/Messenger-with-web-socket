from django.urls import path

from . import views

app_name="main"

urlpatterns = [
    path('', views.index_view, name = 'index'),
    path('start-pv/<str:username>/', views.start_pv_view, name="start_pv"),
    path('start-group/', views.start_group_view, name="start_group")
]