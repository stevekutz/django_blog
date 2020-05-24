#### Project Setup

1) Create environment

    ~~~ bash
    python3 -m venv my_env
    ~~~

3) Activate virtual environment

    ~~~ bash
    source my_env/bin/activate
    ~~~

4) Install Django

    ~~~ bash
    pip install Django
    ~~~


5) Create `mysite` project

    ~~~ bash
    django-admin startproject mysite
    ~~~

6) Run migration to setup tables for applications

- NOTE: you must change directory to the project folder before running migration

    ~~~ bash
    cd mysite
    python manage.py migrate
    ~~~

- The following tables are created

   <img src = "First_Migration_.png"/> 

7) Run the Django development server to verify installation

    ~~~ bash
    python manage.py runserver
    ~~~

#### Setup blog application

1) Create basic strucutre of blog application within project folder

~~~ py
python manange.py startapp blog 
~~~

2) Create the Post model
- The Post model subclasses the `django.models.Model` class in which each attribute field represents a database field
- A `slug` is a short label that contains only letters, underscores, numbers, or hyphens and is used to create SEO-friendly URLs
- the `author` field creates a `many-to-one` relationship where many posts are associated with a specific author(e.g. User)
- the `status` field uses a choices parameter to reference the constant `STATUS_CHOICES` in which only one item can be assigned. This constant is a `tuple of tuples`

    ~~~ py
    from django.db import models
    from django.utils import timezone # needed for timestamp of publish, created, & updated attributes
    from django.contrib.auth.models import User

    # Create your models here.
    class Post(models.Model):
        STATUS_CHOICES = (
            ('draft', 'Draft'),
            ('published', 'Published'),
        )

        title = models.CharField(max_length = 250)
        slug = models.SlugField(max_length = 250, unique_for_date = 'publish')
        author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'blog_posts')
        body = models.TextField()
        publish = models.DateTimeField(default = timezone.now) # date with timezone info
        created = models.DateField(auto_now_add = True) # date when post initially created
        updated = models.DateTimeField(auto_now=True)
        status = models.CharField(max_length = 10, choices = STATUS_CHOICES, default = 'draft')

        class Meta:     # just a class container with some options (metadata)
            ordering = ('-publish', )   # the negative puts in descending order from most recently pubished

        def __str__(self):   # creates a human-readable representation of the object
            return self.title
    ~~~

3) Activate the application

- within `apps.py` is the folowing class

    ~~~ py
    class BlogConfig(AppConfig):
        name = 'blog'
    ~~~

- add the following to `mysite/settings.py` to activate the app. This tells Django tht this app belongs to projects and to load its models

    ~~~ py
    INSTALLED_APPS = [
        'blog.apps.BlogConfig',
        'django.contrib.admin',
    ~~~

4) Create initial migration for the `Post` model 

- this defines how the database will be modified
  
    ~~~ py
    python manage.py makemigrations blog
    ~~~

- to see the SQL(it won't actually be run) that Django will run to implement the migration, run the following

    ~~~ py
    python manage.py sqlmigrate blog 0001
    ~~~


5) Apply the migration

    ~~~ py
    python manage.py migrate
    ~~~

- the database now has the `blog_post` table
 
    <img src = "Post_model_Migration.png"/>


#### Setup Admin

1) Create `superuser`

    ~~~ py
    python manage.py createsuperuser
    ~~~

2) Register models to admin site

- orig

    ~~~ py
    from django.contrib import admin
    ~~~

- updated 
    ~~~ py
    from django.contrib import admin
    from .models import Post

    # Register your models here.
    admin.site.register(Post)
    ~~~
    
3) Launch server and log into admin panel at URL `http://127.0.0.1:8000/admin` too see the admin panel

    <img src = "Admin_panel.png" width = "60%"/>

4) Select Add post and note timezone message

   - message varies depending on your actual timezone

        <img src = "Addpost_timezone_message.png" width = "50%"/>

        - this can be resolved by modifying `TIME_ZONE` in `settings.py` to your actual timezone

        - before

            ~~~ py
            TIME_ZONE = 'UTC'
            ~~~

        - after

            ~~~ py
            TIME_ZONE = 'America/Chicago'
            ~~~

    - However, modifying `TIME_ZONE` can cause issues with Daylight Savings Time. It is recommended to use `UTC` time in the database and convert to `local time` for user interactions. <a href = "https://docs.djangoproject.com/en/3.0/topics/i18n/timezone"> see Time zones Django documentation</a>  

#### Customize admin model

1) Add the following model to `admin.py`

   - note the `admin options` 
     
   -  <a href = "https://docs.djangoproject.com/en/3.0/ref/contrib/admin/"> Django admin options </a>

    ~~~ py
    from django.contrib import admin
    from .models import Post

    # Register your models here.
    # admin.site.register(Post)

    # Custom models 
    @admin.register(Post)   # decorator performs same as admin.site.register(Post)
    class PostAdmin(admin.ModelAdmin):
        list_display = ('title', 'slug', 'author', 'publish', 'status')
        list_filter = ('status', 'created', 'publish', 'author')
        search_fields = ('title', 'body')
        prepopulated_fields = {'slug': ('title',)}
        raw_id_fields = ('author',)
        date_hierarchy = 'publish'
        ordering = ('status', 'publish')
    ~~~

#### Create list & detail views

1) Add the following views

    ~~~ py
    from django.shortcuts import render, get_object_or_404
    from .models import Post

    # Create your views here.
    def post_list(request):
        posts = Post.published.all()
        return render(request, 'blog/post/list.html', {'posts': posts})


    def post_detail(request, year, month, day, post):
        post = get_object_or_404(Post, 
                                slug = post, 
                                status = 'published', 
                                publish__year = year,
                                publish__month = month,
                                publish__day = day)    

        return render(request, 'blog/post/detail.html', {'post': post}) 
    ~~~

2) Add URL patterns for views in the blog app

- this maps URLs to views
- the first pattern does not have arguments
- the second pattern take four arguments
- angle brackets are used to capture values from a URL as a strings
- `path converters` are used to capture values. For example, <int:year> looks for a int parameter and returns an integer. Likewise, <slug:post> matches a slug string
- <a href = "https://docs.djangoproject.com/en/3.0/topics/http/urls/#path-converters"> Django path converters</a>
- `name` maps the view
    ~~~ py
    from django.urls import path
    from . import views

    app_name = 'blog'

    urlpatterns = [
        # post views
        path('', views.post_list, name = 'post_list'),
        path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name = 'post_detail'),
        
    ]
    ~~~

3) Update the project `urls.py`

- add the `include` import

- add the following to the `urlpatterns` variable

- the `namespace` blog allow precise reversing of `names URL patterns`

    ~~~ py

    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('blog/', include('blog.urls', namespace = 'blog')),

    ]

    ~~~

#### Implement Canonical URLs for models

- Canonical means `preferred` and is a unique URL
- the `reverse` method allows URLs to be built using their name and also allows passing additional parameters

- Add the following to `models.py`
- import `reverse`

    ~~~ py
    from django.urls import reverse
    ~~~

- create `get_absolute_url` method to link to specific posts

    ~~~ py

    def get_absolute_url(self):
        return reverse("blog:post_detail",   # define args next, kwargs can also be implmented
                         args=[self.publish.year,
                               self.publish.month,
                               self.publish.day,
                               self.slug ])
    
    ~~~

#### Update the models
- import `reverse`

    ~~~ py
    from django.urls import reverse
    ~~~

- 

#### Create templates for the views    

1) Set up the following folders and files inside the `blog` app

    <img src = 'template_structure.png'/>

- use template tags, template variables, and template filters to create templates

2) Create the `base.html` template

- utilizes `static files`

    ~~~ html
    {% load static %}
    <!DOCTYPE html>
    <html>
        <head>
            <title>{% block title %} {% endblock %} </title>
            <link href = "{% static "css/blog.css"%}" rel = "stylesheet">
        </head>

        <body>

            <div id = "content">
                {% block content %}

                {% endblock %}

            </div>

            <div id = "sidebar">
                <h2> My blog </h2>
                <p> This is my blog </p>

            </div>

        </body>

    </html>
    ~~~

3) Create the `list.html`template

- `extends` allows this template to inherit from the `base.html` file
- 2 template filters are applied in the body of the post

    ~~~ html
    {% extends "blog/base.html" %}

    {% block title %} My Blog {% endblock %}

    {% block content %}
        <h1> My Blog! </h1>

        {% for post in posts %}
            <h2>
                <a href = "{{ post.get_absolute_url }}">
                    {{ post.title }}
                </a>
            </h2>

            <p class = "date">
                Published {{ post.publish }} by {{ post.author }}
            </p>

            {{ post.body|truncatewords:30|linebreaks}}

        {% endfor %}

    {%endblock%}
    ~~~

4) Create `detail.html` template

    ~~~ html
    {% extends "blog/base.html" %}

    {% block title %} {{ post.title }} {% endblock %}

    {% block content %}
        <h1> {{post.title}} </h1>
        <p class = "date">
            Published {{post.publish}} by {{post.author}}
        </p>

        {{post.body|linebreaks}}
    {% endblock %} 
    ~~~

#### Add Pagination

1) In `views.py` add the following import

    ~~~ py
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    ~~~

2) Within `template\blog` create `pagination.html` template

    ~~~ html
    <div class = "pagination">
        <span class = "step-links">
        {% if page.has_previous %}
            <a href = "?page = {{ page.previous_page_number }}">Previous</a>
        {% endif %}

            <span class = "current">
                Page {{page.number}} of {{page.paginator.num_pages}}. 
            </span>

            {% if page.has_next %}
                <a href = "?page={{page.next_page_number }}">Next</a>
            {%endif%}
        </span>
    </div>
    ~~~

3) Within the `list.html` template, add the following to refer to the pagination template

    ~~~ html
    ...
    {% endfor %}

        {% include "pagination.html" with page=posts %}

    {%endblock%}
    ~~~

#### Using Class-based views

- views are implemented as Python objects instead of functions

1) Add `from django.views.generic import ListView` to `views.py`

2) Create the following class-based view in `views.py`

- the following two lines are analogous and create the queryset

    ~~~ py
        model = Post
        # queryset = Post.published.all()
    ~~~

- Although `object_list` is generically created for the query results, using `context_object_name` makes your code easier to follow    

    ~~~ py
    class PostListView(ListView):
        model = Post
        # queryset = Post.published.all()
        context_object_name = 'posts'
        paginate_by = 3
        template_name = 'blog/post/list.html'
    ~~~

3) Modify `blog\urls.py` to use the `PostListView` class

    ~~~ py
    urlpatterns = [
        # post views
        # path('', views.post_list, name = 'post_list'),
        path('', views.PostListView.as_view(), name = 'post_list'),
        ...
    ~~~

4) Update the `list.html` file to receive an obj

- NOTE: you must not put any spaces within `page=page_obj`

    ~~~ html
        {% endfor %}

        <!--  {% include "pagination.html" with page=posts %} -->
        {% include "pagination.html" with page=page_obj %}
    {%endblock%}

    ~~~

5) Add a link to return to the main blogs page

    ~~~ html
    <a href = '/blog'> return to all blogs </a>
    ~~~

### Adding Forms to blog

1) Create a `forms.py` file inside the blog app

- this subclassess the bse Form class
- the CharField typcially renders as a HTML `input` element
- `widget = forms.Textarea` overrides this and renders as an HTML `textarea` element
- email validation is done on anything with `EmailField()`
- <a href = 'https://docs.djangoproject.com/en/3.0/ref/forms/fields/'> Django Form Fields documentation <a/>

    ~~~ py
    from django import forms

    class emailPostForm(forms.Form):
        name = forms.CharField(max_length = 25)
        email = forms.EmailField()
        to = forms.EmailField()
        comments = forms.CharField(required = False, widget = forms.Textarea)
    ~~~

2) Create a view for the form

- add the `EmailPostForm` import to `views.py`

~~~ py
from .forms import emailPostForm
~~~

- Add the `post_share` view

- it has both `request` & `post_id` as parameters
- `get_object_or_404` verifies that post has `published status`
- the same view is used for initial blank forms as well as forms with submitted data
- a `GET` request indicates an empty form has to be displayed
- a `POST` request indicates that valid form data has been submitted for the form to process
- `request.method = POST` distinguishes between these twp scenarios

#### Sending emails with Django

1) Django will write emails to the console if this is added to `settings.py`

    ~~~ py
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    ~~~

2) To use the SMTP server for gmail, add the following with a valid gmail account
- IMPORTANT !! You can hide this info from tracking this sensitive info in github by going into the directory and issuing the following command to halt tracking changes on settings.py

    ~~~ bash
    git update-index --assume-unchanged settings.py
    ~~~

    NOTE - This will restore tracking changes !
    ~~~ bash
    git update-index --no-assume-unchanged settings.py
    ~~~

    ~~~ py
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'valid_gmail_account@gmail.com'
    EMAIL_HOST_PASSWORD = 'password for the account'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    ~~~

3) Modify `views.py`
- import send_mail

    ~~~ py
    from django.core.mail import send_mail
    ~~~

- modify `post_share` in `view.py`

    ~~~ py
    def post_share(request, post_id):
        # Retrieve post by ID
        post = get_object_or_404(Post, id = post_id, status = "published")
        sent = False

        if request.method == 'POST':
            # form was submitted with data
            form = emailPostForm(request.POST)
            if form.is_valid():
                # Form fields passed validation
                cd = form.cleaned_data 
                # ... send email
                post_url = request.build.absolute_uri(post.get_absolute_url())
                subject = f"{cd['name']} recommends you read " f"{post.title}"
                message = f"Read {post.title} at {post_url} \n\n" f"cd['name']\'s comments: {cd['comments']}"
                send_mail(subject, message, 'sktestdjango@gmail.com', [cd['to']])
                sent = True

        else:  # show blank form
            form = EmailPostForm()        

        context = {'post': post, 'form': form, 'sent': sent}

        return render(request, 'blog/post/share.html', context)  
    ~~~

4) Add the path in `/blogs/urls.py`    

    ~~~ py
    urlpatterns = [
        # post views
        # path('', views.post_list, name = 'post_list'),
        path('', views.PostListView.as_view(), name = 'post_list'),
        path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name = 'post_detail'),
        path('<int:post_id>/share/', views.post_share, name = 'post_share'),
    ]
    ~~~