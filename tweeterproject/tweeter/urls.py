from django.urls import path
from . import views

app_name = "tweeter"

urlpatterns = [
    path('', views.home, name="homepage"),
    path('tweets/', views.tweets, name="tweets"),
    path('create/', views.createtweet, name="create_tweet"),
    path('edit/<int:postid>/', views.edittweet, name="edit_tweet"),
    path('delete/<int:postid>/', views.deletetweet, name="delete_tweet")
]