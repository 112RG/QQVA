# QQVA
Capstone project. Rylee and Peter

PYTHON 3.9

# install reqs first
```pip install -r requirements.txt```

# Startup development

```python manage.py runserver```

# Start server WITH websocket server

```daphne -p 8000 qqva.asgi:application```

# start server WITH websocket server on codespaces

```python -m daphne -p 8000 qqva.asgi:application```

# Python needs to migrate

```python manage.py migrate```

# when changes have been made to the main folder you need to migrate the changes then ^ again

```python manage.py makemigrations main```

# create username and password for django admin page

```python manage.py createsuperuser```

# install crispyforms for easy styling

```pip install django-crispy-forms```