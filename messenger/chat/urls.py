from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('pv/<int:pv_id>/', views.pv_view, name="pv"),
]