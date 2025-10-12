# Tutorial for Django


# The Beginning

1. Choose a containing folder for all django projects
2. inside it - django-admin startproject firstproject
3. then - django-admin startapp firstapp

	**structure-**
	```
		Django-folder
			->firstproject
				->firstproject
					->urls
					->wsgi
					->etc
				->firstapp
					->views
					->tests
					->etc
					
			->secondproject
				...
	```
4. Create urls.py in firstapp
5. Create 'templates' folder in firstapp, then put a html file on it. (For now index.html)

6. Create a view of index.html-
	**views.py (firstapp)**
	```python
	from django.shortcuts import render
	
	def home(request):
		return render(request, "index.html")	#It will look into templates folder for index.html
	```

7. Then we have to map it in firstapp/urls.py -	<br/>
	_When firstapp will be asked for home then it will check views (view.home -> home() function) then templates and then will return index.html_
	```python
	from django.urls import path
	from . import views
	
	urlpatterns = [
		path("", views.home, name="homepage")
	]
	```
	
8. Then map firstapp to firstproject-
	_When django will be asked for app, it will check firstproject urls. firstproject urls.py is referencing it to firstapp urls.py ._
	```python
	from django.urls import path, include
	
	urlpatterns = [
		...admin...
		path('app/', include("firstapp.urls"))	#Note app/ -> '/' is important. Using slash you can enter different webpages in firstapp
	```
	
9. In firstproject.settings register your app-
	In INSTALLED_APPS, add "firstapp" -
	```
		INSTALLED_APPS = [
			... ,
			... ,
			'firstapp',
		]
	```
	
10. Now check **_localhost:8000/app_**

**Notes-**
	i. If in firstproject.urls path('', ....) -> then you have to just enter **_localhost:8000_**
	ii. **Slash importance** - In firstproject.urls - app/ not app. It will still work, but you will not be able to name the different webpages. As '/' means anything after 'app'.
		-> Now if you named "home" your firstapp home, then enter **_localhost:8000/app/home_**
		
11. **Static files** - Make a folder 'static' in app. Put your css, js, etc files in static. In settings.py check if STATIC_URL = 'static/' exists, if not then write.
	```
	firstapp
		->static
			->base.css
			->base.js
	```
	Then in the html files include static files -
	```
	{% load static %}
	<link rel="stylesheet" href="{% static '/base.css' %}">
	```
	**_If static file is created while server is running then static files might not show up. Restart the server._**
	

# Django admin panel

1. Create super user-
	```bash
	python3 manage.py createsuperuser
	```
	Then fill necessary details
	
2. Runserver, then type localhost:8000/admin


# Models

1. On models.py on app create table columns
	```python
	from django.db import models
	from django.contrib.auth.models import User	#To make foreign key with this table and User table

	# Create your models here.
	class Post(models.Model):   #New table
	    stat_ch = [				#Iterable of iterables
		("draft", "Draft"),
		("published", "Published")	#1st is option that is stored on db, 2nd is option that will be showed to user
	    ]

	    title = models.CharField(max_length=30, primary_key=True)
	    content = models.TextField()
	    status = models.CharField(max_length=1, choices=stat_ch, default="draft")
	    author = models.ForeignKey(User, on_delete=models.CASCADE)
	```
	Then 
		-> python3 manage.py makemigrations
		-> python3 manage.py migrate
	
	
	
	
	
	
	
	
