release: python manage.py migrate --no-input --settings=comm.production
web: gunicorn comm.wsgi --log-file -
