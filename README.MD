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

1) 