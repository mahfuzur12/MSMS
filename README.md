# Team *<enter team name here>* Small Group project

## Team members
The members of the team are:
- *<Mahfuzur Rahman>*
- *<Levi Pemindjafol Yeo>*
- *<Haris Islam Malik>*
- *<Mohammad Ruhan-Ur Rahman>*

## Project structure
The project is called `msms` (Music School Management System).  It currently consists of two apps `lessons` and `msms` where all functionality resides.

## Deployed version of the application
The deployed version of the application can be found at *<[enter URL here](URL)>*.

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Migrate the database:

```
$ python3 manage.py migrate
```

Seed the development database with:

```
$ python3 manage.py seed
```

Run all tests with:
```
$ python3 manage.py test
```

TESTS MIGHT GIVE YOU AN ERROR OR FAILURE BUT THE APP WORKS FINE.

## Sources
The packages used by this application are specified in `requirements.txt`

