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
	    author = models.ForeignKey(User, on_delete=models.CASCADE)
	```
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
		
	**Note** - The text must not include space. Also ID can be used here. 


6. **Link each posts from main listing page** - **_(Get absolute URL)_**

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
				return reverse("app:eachposts", args=[self.id])
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
	
	
	**All important files** -
	app.views -
	```python
	from django.shortcuts import render, get_object_or_404
	from .models import Post

	# Create your views here.
	def home(request):
	    all_posts = Post.objects.all()

	    return render(request, "home.html", {"posts":all_posts})

	def each_post(request, postid):
	    single_post = get_object_or_404(Post, id=postid)
	    return render(request, "blogpost.html", {"post":single_post})
	```
	    
	app.urls -
	```python
	from django.urls import path
	from . import views

	app_name="blog"

	urlpatterns = [
	    path('', views.home, name="homepage"),
	    path('<slug:postid>/', views.each_post, name="each_posts")
	]
	```
	
	app.models -
	```python
	from django.db import models
	from django.contrib.auth.models import User
	from django.urls import reverse

	# Create your models here.
	class Post(models.Model):
	    status_choices = [
		("draft", "Draft"),
		("published", "Published")
	    ]

	    title = models.CharField(max_length=30)
	    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
	    content = models.TextField()
	    status = models.CharField(max_length=10, choices=status_choices)

	    def __str__(self):
		return self.title

	    def get_absolute_url(self):
		return reverse("blog:each_posts", args=[self.id])    #Get absolute url of each posts using id
	```
	
	home.html -
	```html
	<body>
	    home
	    {% for i in posts %}

	    <a href="{{i.get_absolute_url}}">Link</a>

	    {% endfor %}
	</body>
	```
	
	singlepost.html -
	```html
	<body>
	    {{post.title}}
	    {{post.author}}
	    {{post.content}}
	</body>
	```
	
7. **Template inheritance** -

8. **Model manager** -


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
	``python
	Post.objects.order_by('status')
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






	

