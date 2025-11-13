from django.urls import path
from . import views

app_name="crudapp"

urlpatterns = [
    path('', views.home, name="homepage"),
    path('pathtosubmit/', views.takeData, name="takedata"),
    path('gallery/', views.gallery, name="gallery"),
    path('action/', views.userAction, name="userAction"),
]