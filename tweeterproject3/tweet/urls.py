from django.urls import path
from . import views

app_name = "tweet"

urlpatterns = [
    path('', views.home, name="homepage"),
    path('create/', views.createpost, name="createpost"),
    path('edit/<int:postid>/', views.editpost, name="editpost"),
    path('del/<int:postid>/', views.delpost, name="delpost"),

    path('register/', views.register, name="register")
]