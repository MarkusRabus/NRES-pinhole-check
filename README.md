# NRES-pinhole-check

Django application to check the pinhole centering during the night.

## Prequisites:

1. gunicorn server

2. Python 3.5 or higher

3. Django, imageio, requests, tempfile

4. Jupyter (optinal to run the jupyter notebooks)

A file with archive user name and password at in your home directory. `/home/.../userdata.dat`

## Run the django application with gunicorn:

`gunicorn NRES.wsgi -k gevent --name bullseye --bind XXX.XX.X.XX:8000 --workers 4 --timeout 300`

Replace X's with IP address.




## Create new database with Django:

```
python manage.py makemigrations bullseye
python manage.py sqlmigrate bullseye 0001
python manage.py migrate
```
The `gif` files will be saved in the directory `Django_Projects/guider_gifs/`+date.


