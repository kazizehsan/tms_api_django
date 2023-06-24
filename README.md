# Task Management System

## Environment setup

From the project directory, run the following
```
pipenv install
pipenv shell
```

## Database and Superuser setup

The Django superuser is required to assign registered users to different groups (Manager, Officer) using the `PUT /account/{id}` API. Normal users cannot assign groups to themselves.

From the project directory, run the following
```
cd tms
python manage.py migrate
python manage.py createsuperuser
```

## Run API server

From the project directory, run the following
```
cd tms
python manage.py runserver
```

### Documentation

Visit `http://127.0.0.1:8000/redoc/`


## Tests

From the project directory, run the following
```
cd tms
python manage.py test
```