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

