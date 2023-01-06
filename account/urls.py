from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('', views.login1_view, name='account'),
    path('validate/', views.login2_view, name="validate"),
    path('register/', views.login3_view, name="register"),
]