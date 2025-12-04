# Tutorial for Django
**This tutorial contains errors solution too**


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
	i. If in firstproject.urls path('', ....) -> then you have to just enter **_localhost:8000_**	<br/>
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

1. **Create super user**-
	```bash
	python3 manage.py createsuperuser
	```
	Then fill necessary details
	
2. Runserver, then type localhost:8000/admin
	**Note** - Superusers are specific for a specific project. Not available to all projects.


# Models

1. On models.py on app **create table** columns
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
	    author = models.ForeignKey(to=User, on_delete=models.CASCADE)	#CASCADE means if user gets deleted, all records associated with it will also be deleted.
	```
	
	**Notes** - 
		1. **CASCADE** means if user gets deleted, all records associated with it will also be deleted.
		
		2. On datetime field, **auto_now_add** - adds time when record is being 1st time created. **auto_now** - adds time whenever it's updated.
		
		3. **null=True** - allows db to store null values. **blank=True** - allows the field to be empty in the form.
	
	**_Django automatically creates id primary key if other field is not marked as primary key explicitly_**	<br>
	Then-
	```bash
		python3 manage.py makemigrations
		python3 manage.py migrate
	```
	Then register the table-
		On admin.py -
		```python
		from django.contrib import admin
		from .models import Post		#Name of the table
		
		admin.site.register(Post)
		```
	Now from admin panel open Table and 'Add Post'. **_(Optional 'Add Post' from admin panel directly, development purpose)_**
	
2. **Read table** - (If you created some rows through admin panel)
	On app.views -
	```python
	from .models import NameOfTable
	
	def home(request):
		all_posts = NameOfTable.objects.all()
		
		return render(request, "index.html", {"all_data":all_posts})
	```
	Then in html -
	```html
	<body>
		{% for i in all_data %}
		
		{{i.row1}}
		{{i.row2}}
		
		{% endfor %}
	```
	
3. **Change display style** - On admin page table, rows title will be -> 'Post object(1), (2) ...' (if id is the primary, otherwise whatever is the primary key it will show that).
	To change that -
	```python
	class NameOfTable():
		...
		...
		def __str__(self):
			return self.title
	```
	
4. **Access record with id in url** - _http://localhost:8000/admin/blog/post/_ -> Where 'post' is table name. Then add the id no. you want to find like - _http://localhost:8000/admin/blog/post/2_

5. **Retrieve all data of a single record using a column in url** -
	**Using Django's slug field**	<br/>
	1. In urls.py app-
		```python
		path("<slug:post_name>/", views.eachpost, name="eachposts")	# 'slug' captures the text on the url and sends it to the views. (post_name is just a var)
		```
		<br/>
	2. In views.py -
		```python
		from django.shortcuts import get_object_or_404
		from .models import NameOfTable
		
		def eachpost(request, post_name):
			post = get_object_or_404(NameOfTable, columnName=post_name, otherColfor_filter="filtrationtext")
			return render(request, "singlepost.html", {"post":post})
		```
		Then type _localhost:8000/1_ or _localhost:8000/text1_ (If no extra url section is added for app, otherwise include them)
		**We can use Table.objects.get(args) too, instead of get_object_or_404.**
		
	**Note** - The text must not include space. Also ID can be used here. 


6. **Link each posts from main listing page** - **_(Get absolute URL, Slug)_**

	**Note** - For step 6, step 5 is needed.
	
	1. On app.urls write -
		```python
		from ... import ....
		
		app_name = "app"	#Name can be anything related to your app
		
		path("", views.home, name="homepage")
		path("<slug:post_name>/", views.eachpost, name="eachposts")	# *1
		
		```
		<br/>
	2. Now get absolute url. In models.py add -
		```python
		from django.shortcuts import reverse
		
		class Table(models.Model):
			col1
			col2
			...
			
			def get_absolute_url(self):
				return reverse("app:eachposts", args=[self.id])		# appname : slug's viewname(name="...")
		```
		<br/>
	3. views.home -
		```python
		all_posts = Post.objects.all()
		return render(request, "home.html", {"posts":all_posts})
		```
	   home.html -
	   	```html
	   	{% for i in posts %}
	   	
	   	<a href="{{i.get_absolute_url}}">Link to post</a>
	   	
	   	{% endfor %}
	   	<br/>
	4. Then redirect to 'singlepost.html' like step 5.
	
	_Now we can click the links on homepage to go to each posts page_
	
	**Process -**	<br>
	1. In homepage all records are shown. Then get_absolute_url function is used from models specific table.
	2. That function uses reverse and the records cols to get absolute url.
	3. When that url is used in anchor, it asks urls slug field.
	4. Slug field checks request and sends it to views with the parameter provided in url
	5. Then views finds the object record with that parameter and sends the record data to another webpage.
	
	
7. **Handling multiple tables** -

	models.py-
	```
	class Post(models.Model):
	    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
	    content = models.TextField(max_length=240)
	    image = models.ImageField(upload_to='photos/')
	    created_at = models.DateTimeField(auto_now_add=True)
	    modified_at = models.DateTimeField(auto_now=True)

	    def __str__(self):
		return self.content[:10]+str(self.id)

	class Interaction(models.Model):
	    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='interaction')
	    likes = models.IntegerField()

	    def __str__(self):
		return self.post.content[:5]+" "+str(self.likes)
	```
	**Note** - Related name must be used on foreign keys only. It helps to query fields on templates.
	
	1. **In views merge two table queries in a dict, then pass it to template** -
		views-
		```
		posts = Post.objects.all()
		interactions = Interaction.objects.all()
		
		post_data = {'posts':posts, 'interactions':interactions}
		
		return render(req, 'abc.html', post_data)
		```
		
	2. **Now we can access values of both tables because they are interconnected** -
		```html
		{% for post in posts %}
			{{post.content}}
			
			{{post.interaction.first.likes}}
		{% endfor %}
		
	**Notes** -
		1. To access 'Interaction' table from 'Post' we need to add **'related_name'** on the foreignkey. Then using that name we can access all fields of the table.

	
# Other ways to pass param to urls -
	1. In urls -
	```python
	app = 'post'
	
	urlpatterns = [
		path('edit/<int:post_id>/', views.editpost, name='edit_post'),
		path('delete/<int:post_id>/', views.delpost, name='del_post'),
	]
	```
	2. In template -
	```html
	{% for i in data %}
		<a href="{% url 'post:edit_post' i.id %}">Link</a>
	{% endfor %}
	```
	**Notes** - 
		1. Url on template must be 'app_name:view_pattern_name>'.
		
		2. Slug means any data type, where int speifies that the var will have int type.
		
		3. In this method, don't need to create get_absolute_url.
	
	
# Template inheritance -

1. Create a base.html file in templates. (This will contain all necessary contents that will be inherited to other templates)

2. **Definitions** -
	```
	{% extends 'base.html' %}	//Used in working templates to inherit everything from base template
	
	{% block var %} {% endblock %}	//Works as a variable for the base file to put content according to the page. Used in 
	```
	
   **Working** -
	_base.html_
	```html
	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <meta name="viewport" content="width=device-width, initial-scale=1.0">
	    <title>{% block title %} {% endblock %}</title>
	</head>

	<body>
	    {% block body %}
	    {% endblock %}
	</body>
	</html>
	```
	
	_home.html_
	```
	{% extends 'base.html' %}
	
	{% block title %}Home{% endblock %}
	
	{% block body %}
	hello
	{% endblock %}
	```
	
  **Notes** - 
	1. If you don't include a block in working template it will not be used.
	
	2. If on base file something is written between blocks, it will act as a default content. If nothing is added on working files then default content will show up.


# Model manager -


# SqLite3 Django shell queries-

1. **To open django shell** - python3 manage.py shell

2. **Import models** - from appname.models import Table

3. **Select * from table** - 
	```python
	a = Table.objects.all()		#Returns queryset object
	for i in a:
		print(i.id)
		print(i.title)
	```
	Or,
	```python
	for i in a:
		print(i)	#It will return all post objects (If used dunder __str__ it will show according to that)
	```
	Or Print all values inside queryset without loop,
	```python
	Post.objects.all().values()	#It will show all col values for each record
	```
	
4. **Create** -
	```python
	new_record = Table(title="New title", content="New content")
	
	new_record.save()	#No data will be created until saved
	```
	
5. **Select * from table where title='abc'** - (Where clause)
	```python
	Post.objects.get(title='abc')
	
	Post.objects.get(title='abc').content	#Access individual columns after filtering
	```
6. **Filter** -
	```python
	Post.objects.filter(id=1)
	
	Post.objects.filter(id=1).filter(title='abc')	#Multiple filters
	
7. **Exclude records** -
	```python
	Post.objects.exclude(id=1)	#Exclude id=1 record
	
	Post.objects.filter(publish_date__year=2025).exclude(title='abc')	#Filter 2025 records then exclude title 'abc'
	```
	
8. **Order by clause** -
	**Ascending order** -
	``python
	Post.objects.order_by('status')	#status -> field name
	```
	
	**Descending order** -
	``python
	Post.objects.order_by('-status')
	```
	
9. **Delete** -		(After deleting a record the id also gets deleted)
	```python
	post = Post.objects.get(id=1)
	
	post.delete()
	
	#To delete all records
	Post.objects.all().delete()
	
	```
	
# Request.GET method

**Retrieve parameters sent by form**

1. Make html form. name in input tag is must as it will be used to match in request querydict.
	```html
	<form action="/calculate" method="get">
		<input name="fname">
	```

2. Create a new url path that matches the form action

3. Create new view.
	```python
	def home(req):
		...
		
	def new_view(req):
		fname = req.GET.get('fname')
		lname = req.GET.get('lname')
		
		return HttpResponse(fname+lname)
		
	```
	
# Request.POST method

1. On html include -
	```html
	<head>
	{% csrf_token %}
	...
	</head>
	
2. On javascript file
	```javascript
	const csrf = document.querySelector("[name=csrfmiddlewaretoken]");
	```

3. On views -
	**If JS file sends _application/x-www-form-urlencoded_**
	```python
	def func(request):
		a = request.POST.get("abc")
	```
	**If JS file sends _application/json_**
	```python
	def func(request):
		data = json.loads(request.body.decode("utf-8"))
		a = data.get("abc")
	```

	
# Django static caching problem

**Problem** - The browser will cache the static files if used so many times (On local dev). And then if you change something on css after it is cached, the changes will not reflect.
**Sol.** - Open webpage and clear cache by Ctrl+F5.


# File field -

	**Content type should be 'multipart/form-data'**
	```python
	#On models
	resume = models.FileField(upload_to="uploads/",blank=True)
	```
	**The *'uploads_to'* attribute will create a new folder in /root to save uploaded files.**
	
	**On views** -
	```python
	file = request.FILES.get("files")
	name = request.POST.get("name")
	
	print(name, file.name)
	
	new = Table(file_entry = file)
	new.save()
	```
	
# TailWind CSS in Django -

**Ref** - https://pypi.org/project/django-tailwind/
**_*Node must be installed first_**

1. -> pip install django-tailwind

2. Open any project then on settings.py add-
	```python
	INSTALLED_APPS = [
		...,
		'tailwind',
	]
	```
	
3. -> python3 manage.py tailwind init

	_Add the tailwind app name_-
	```python
	INSTALLED_APPS = [
		...,
		'tailwind',
		'theme',	#If configured app name is theme during init
	]
	
	TAILWIND_APP_NAME = 'theme'
	```
	
4. -> python3 manage.py tailwind install

5. Add these on **head** (When added before doctype, the page will open in quirks mode in browser, without xhtml) -
	```html
    	<!doctype html>
    	<head>
    		{% load tailwind_tags %}
	    	{% tailwind_css %}
	</head>
    	
    	<p class="bg-orange-200">Hello</p>
    	```

6. On 1st console -
	-> python3 manage.py runserver
   On 2nd console -
   	-> python3 manage.py tailwind start
   	
   **If it's not working then restart server(1st console).
   
7. **(Optional)** If not working -
	1. Set proper node env var.
	
	2. console - whereis node
	
	3. On settings.py after 'TAILWIND_APP_NAME', add 'NPM_BIN_PATH = /path of node/'.
	
   **Notes** -
   	1. Tailwind and static file css can cause problems, like css file not loading current props after loading. So you can restart the server.
	
	
# Django Forms

_Helps to create forms in frontend using existing models from backend_

**Create form**
1. Create 'forms.py' on app (where urls.py exists)
	**Use existing models for forms** -
	```python
	from .models import MyModel
	from django import forms
	
	class FormName(forms.ModelForm):
		class Meta:
			model = MyModel
			fields = ['name', 'title', 'image']	# Choose specific fields from models that you want fields for in form
	```
	
2. Add form on views and pass it to template -
	views.py-
	```python
	from .forms import FormName
	
	def createform(request):
		if request.method == "POST":		#If form has been submitted, it will be a post request
			form = FormName(request.POST, request.FILES)	# Pass what data types it will handle
			if form.is_valid():
				new_record = form.save(commit=False)	# commit=False when you want to add more field data that doesn't exist on form
				new_record.user = request.user		# saving user info on models, user field doesn't exist on forms
				new_record.save()
				
				return redirect("")
		else:
			form = FormName()		# If just the url has been called then return the form.
			
		return render(request, "abc.html", {"form":form})
	```
	**Notes (file not saving issue)** - **for create post template, must add enctype="multipart/form-data". Other wise file will not be saved and will be empty every time clicked on submit btn.**
	
**Edit form** -

1. Pass an instance of the record -
	views.py -
	```
	def editform(request, postid):
		record = get_object_or_404(Table, id=postid, user=request.user)
		if request.method == 'POST':
			form = Form(request.POST)
			form.save()
			
			return redirect("/")
		else:
			form = Form(instance=record)
		return render(..., {'form':form})
	```

	**Notes** -
		1. every request has a user info, can be accessed by **request.user**.
		
**Form rendering** -

_Can be rendered using just {{form}}, but this has limited functionality in design_

**This will render every single component of form one by one, then we can apply styling.

1. Old < v5.0 -
	```html
	<form>
		{{form.email.label_tag}}
		{{form.email}}
		
		{% if form.email.errors %}
                    <p class="text-ptext text-red-500">{{form.email.errors}}</p>
                {% endif %}
	```
	
2. v5.0
	```html
	<form>
	{% for field in form %}
		
		{{field.as_field_group}}
		
	{% endfor %}
	</form>
	```
		

# Media configuration

1. In settings.py add-
	```python
	MEDIA_URL = '/media/'
	MEDIA_ROOT = BASE_DIR / 'media'
	```
	
2. In root urls.py add -
	```python3
	from django.conf import settings
	from django.conf.urls.static import static
	
	urlpatterns = [
		...
	] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)	# Add media paths
	```
	
   **Notes** -
   	1. media_root - all media images are stored here.
   	
   	2. media_url  - django checks for images here, when serving to template.
   	

# Simple Lazy object error -
**Error** - "<SimpleLazyObject: <django.contrib.auth.models.AnonymousUser object at 0x71905047eef0>>": "Tweet.user" must be a "User"

This error occurs when you are not signed in, nor you have designed login section to redirect when user is logged out. When logged out d=jango returns Anonymous in request.user.	<br/>
So in the same tab go to admin panel, if it asks to login, then login. The problem should be gone for some time (probably 30mins).


# Login protect contents -

	views.py-
	```python
	from django.contrib.auth.decorators import login_required
	
	@login_required
	def createpost():
		...
	```
	**Now when no user is logged in django will redirect user to login page for that view. Redirects to default url accounts/login.**
	
	
# User registration, login, logouts -

	**To make pages for login, register etc the templates must be in root folder** -
	```python
	->projectname
		->projectname
			settings.py
			asgi.py
			...
					
		->app
			->templates
				->home.html
				->about.html
				
		->db.sqlite3
		
		->templates
			->registration
				->login.html
				->register.html
				->logout.html		//Optional
	```
	**Note** - Django auth looks for templates in templates/registration by default.
	
	**Settings.py** -
	On templates section specify where to look for templates first -
	```
	TEMPLATES = [
		'DIRS' : [BASE_DIR / 'templates']
		
	]
	
	
	LOGIN_URL = 'accounts/login'
	
	# LOGIN_REDIRECT_URL = 'home_view_name'	# The view name for a page where you want to redirect, in views.py
	
	LOGOUT_REDIRECT_URL = '/'	# home page url
	```
	**Notes** - login redirect, logout redirect pages are optional. Django automatically redirects to the previously clicked page which was login protected, when logging in.
	
	**Urls.py projects** -
	add another path for accounts
	```
	path('accounts/', include('django.contrib.auth.urls'))
	```
	
	**Forms.py** -
	```python
	from django import forms
	from django.contrib.auth.forms import UserCreationForm
	from django.contrib.auth.models import User
	
	class UserRegistrationForm(UserCreationForm):
	email = forms.EmailField()
		class Meta:
			model = User
			fields = ('username', 'email', 'password1', 'password2')
	```
	**Note** - UserCreationForm is a builtin form. When referencing builtin forms we have to use tuples. For custom forms use list.
	
1. **Register** -
	urls.py app -
	```python
	path('register/', views.register, name='register_page')
	```
	
	views.py -
	```python
	from .forms import UserRegistrationForm
	from django.contrib.auth import login
	
	def register(request):
		if request.method=='POST':
			form = UserRegistrationForm(request.POST)
			if form.is_valid():
				user = form.save()
				
				login(request, user)
		else:
			form = UserRegistrationForm()
		
		return render(request, 'registration/register.html', {'form':form})
	```
	
	register.html -
	```html
	<form method="post" enctype="multipart/form-data" class="w-full h-max flex flex-col justify-center items-center">
		{% csrf_token %}
		
		{% for field in form %}

			{{field.as_field_group}}

		{% endfor %}

		<button class="btn btn-success shadow-none w-20">Register</button>
	 </form>
	 ```
	 
	**Notes** -
		1. login method takes request and the user, from these it automatically logs in the user. form.save returns instance of the user, otherwise this error will appear 'ModelFormOptions' object has no attribute 'pk'.
		
		2. Here 'registration/register.html' because settings is BASE_DIR / templates, which points to root/templates and in templates/registration register.html exists.
		
2. **Login** -

	Don't need to have any views for this.
	
	1. Just create a login.html in registrations. Use forms like other pages.
	
	2. The views which are login protected will automatically redirect user to login page.
	
	3. To manually go to login page - _url:8000/accounts/login_.
	
3. **Logout** -

	Don't need to have any views for this. Logout is a form provided by django.
	
	1. Use a post form - action -{% url 'logout' %}, with csrf token, then use a submit button.
	
4. **Conditional rendering for specific users** -

	1. If you have for loop, and want to show some elements conditionally then -
		```html
		{% for i in posts %}
			{% if i.user == user %}
				
				<button>Show it to user</button>
				
			{% else %}
				show nothing
				
			{% endif %}
				
		{% endfor %}
		```
		
	**Notes** - 
		1. It's optional to use else, but must to use endif.
		
		2. user can be always accessed, because it's part of request.
		
	
	2. **Checking if user is logged in** -
		```html
		{% if user.is_authenticated %}
			<a href="{% url 'logout' %}>Logout</a>
		{% else %}
			<a href="/accounts/login">Login</a>
			<a href="/register/">Register</a>
			
		{% endif %}
		

# Universally Unique ID -

It is a 128bit 32 char long string, to act as a id. This eliminates predictability of id, removing the use of auto incrementing id, improving security.

	models.py -
	```python
	import uuid
	
	class Post(models.Model:
		id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
		
	```
	
1. **It can be defined in a base model and called to main model from the base model** -
	```
	->PROJECT root
	->base
		->models.py -
			import uuid
	
			class BaseModel(models.Model:
				id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
				... additional fields ...
				
				class Meta:
					abstract = True
		
	->app
	->project
	```
	
	**Note - Abstract in meta class makes django to think of this as a class not a model**
	
	app-models.py -
	```
	from base.models import BaseModel
	
	class Post(BaseModel):
		name = models.CharField(...)
	```
	
	**Note** - These are called _helpers_, they improve code reusability.

**UUID versions**
```
Version		Description									Use Case
UUID1		Generated using the current timestamp and the MAC address of the host.		Suitable for scenarios requiring time-based sorting.
UUID2		Similar to UUID1 but includes POSIX UID/GID. Rarely used.			Specific use cases in DCE security.
UUID3		Generated using an MD5 hash of a namespace and a name.				Useful for consistent UUIDs based on input.
UUID4		Randomly generated UUID.							Commonly used for general purposes due to its randomness.
UUID5		Similar to UUID3 but uses SHA-1 hashing instead of MD5.				Provides consistent UUIDs based on input.
```
		
		
# Table's reverse relations-

	models.py-
	```
	from django.db import models
	from django.contrib.auth.models import User

	# Create your models here.
	class Category(models.Model):
	    name = models.CharField(max_length=30)
	    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
	    created_at = models.DateTimeField(auto_now_add=True)
	    modified_at = models.DateTimeField(auto_now=True)

	    def __str__(self):
		return self.name+"("+self.user.username+")"

	class Portfolio(models.Model):
	    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
	    title = models.CharField(max_length=50)
	    description = models.TextField(max_length=240)
	    file = models.FileField(upload_to='photos')
	    created_at = models.DateTimeField(auto_now_add=True)
	    modified_at = models.DateTimeField(auto_now=True)
	    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='category_on_portfolio')

	    def __str__(self):
		return self.title
	```
	
	
# Django ORM(object relational mapping) - Advanced queries

1. Limit records - records = Model.objects.all()[0:100]		**Select only 100 records through slicing**

2. Filter by greater or less than - 
	i. records = Model.objects.filter(views__gte = 10)	**Select records which 'views' field values are greater than equals 10. double '_' means a speial django keyword.**
	
	ii. records = Model.objects.filter(views__gte = 10).exclude(title='abc')	**Select 'views'>=10 but exclude title 'abc'.**
	
	iii. records = Model.objects.filter(views__lte = 40)	**Select records with 'views'<40.**
	
**New database and tables** -

1. Department
	department = charfield
	
2. 







	

