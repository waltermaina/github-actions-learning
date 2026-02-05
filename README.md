# Django Application with Pipenv

This is a simple Django application created to verify that Django has been installed correctly and is working with pipenv for environment management.

## Project Structure

```
github-actions-learning/
├── Pipfile              # Pipenv configuration file
├── Pipfile.lock         # Locked dependencies
├── manage.py            # Django management script
├── myproject/           # Django project directory
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py      # Django settings (includes 'home' app)
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py
├── home/                # Django app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py          # App URL configuration
│   └── views.py         # Main view
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.14.2
- pipenv

### Installation

1. Install Django using pipenv:
   ```bash
   python -m pipenv install django
   ```

2. Activate the virtual environment:
   ```bash
   python -m pipenv shell
   ```

3. Run the development server:
   ```bash
   python -m pipenv run python manage.py runserver
   ```

### Usage

- Visit http://127.0.0.1:8000/ to see the welcome page
- Visit http://127.0.0.1:8000/admin/ to access the Django admin interface

### Commands

- Start development server: `python -m pipenv run python manage.py runserver`
- Apply database migrations: `python -m pipenv run python manage.py migrate`
- Create superuser: `python -m pipenv run python manage.py createsuperuser`

## Features

- Simple Django application with a basic view
- Uses pipenv for environment management
- Includes proper URL routing
- Database migrations applied
- Ready for further development

## Notes

This application serves as a basic Django setup to verify installation and can be extended for more complex functionality.