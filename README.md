# Wilsonads Ecommerce Website

### Superuser
*username: admin
*password: 1234

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
1. Install Python & Pip
2. Setup virtual environment
```bash

# Create virtual environment
py -m venv myvenv

# Activate virtual environment
source myvenv/Scripts/activate
```

### Installation and Setup
1. Clone repository
    ```
    git clone "*insert link here"
    ```
2. Install requirements
    ```
    pip install -r requirements.txt
    ```
### Developer's Tools (Running)
1. Run when changing model.py
    ```
    manage.py makemigrations
    manage.py migrate
	```
2. Run server
	```
    manage.py runserver
    ```

Helpful links
- https://github.com/divanov11/django_ecommerce_mod5
