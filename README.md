# Olist bookstore

This app is a fork of https://github.com/olist/work-at-olist.

The setup used for build this app was:
- Macbook Pro 2015
- OSX 10.15.4 
- Visual Studio Code 1.44.2
- Python 3.8.2 

Libs:
- black 19.10b0
- Django 3.0.5
- djangorestframework 3.11.0
- drf-yasg 1.17.1
- coverage 5.1

## Instalation

To install app, first create a virtual environment:
```
python3.8 -m venv venv
```

Then activate it:
```
source venv/bin/activate
````

Then install requirements:
```
pip install -r requirements.txt
```

## Testing

To run all the tests run:
```
python manage.py test
```

To check testing coverage run 

```
coverage run --source='.' manage.py test myapp
```

Then to check report
```
coverage report
```

## Generating database

To generate/update test sqlite database, apply migrations:

```
python manage.py migrate
```

## Importing initial data

This app can import initial csv data of authors.

For it, you should have a csv with a a column named "name"

Then you can run 
``` 
python manage.py import_authors file.csv
```

To import all authors from this file

You can also customize the database save chunk size, for larger loads

``` 
python manage.py import_authors file.csv --chunk-size 100000
```

## Running

To run locally, just start django server
```
python manage.py runserver
```

## Documentation

You can find a nice swagger documentation on http://localhost:8000/swagger/
(there is also a offline version [here](swagger.json))

There is also a redoc documentation on http://localhost:8000/redoc/

Or yet, the broseable API on http://localhost:8000/bookstore/