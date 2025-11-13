from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path('', views.forms, name="forms"),
    path('store/', views.store, name="store"),
    path('resume/', views.resume, name="resumepage")
]