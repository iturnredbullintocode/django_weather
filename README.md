Dockerized weather app
=====================
Django - Postgres - Memcached

running the app
--------------------
- Don't use any of these variables/settings in production, for the sake of speed they are sitting in the .env file, and the file is being git tracked.
- Assuming development environment will be needed friday, so django toolbar is currently set to on, as well, and project settings are dev mode.
- you will need Docker installed to run the app
- simply clone the entire repo and `docker-compose build` and `docker-compose up -d`
- three docker containers will spin up:
    - django on http://localhost:9100
    - postgres on http://localhost:9200
    - memcached server on http://localhost:9300
- do `docker ps` and grab the container id of the django container
- execute a database migration command inside the django container via `docker exec -it DJANGO_CONTAINER_ID_GOES_HERE python manage.py migrate`
- do `docker ps` and grab the container id of the memcached container
- do `docker container inspect MEMCACHED_CONTAINER_ID_GOES_HERE` and toward the end it will show the specific ip address that is inside the docker container that it is running on - something like `192.168.48.2`
- take memcached's IP address and add it to the `.env.web-dev` file like `MEMCACHED_DOCKER_IP=192.168.48.2`


troubleshooting
------------------
- please note that I could automate and improve a lot of these issues but its out of the scope of a 4 hour project
- sometimes, the postgres container takes a long time to load up, and django gets an error like `django.db.utils.OperationalError: FATAL:  the database system is not yet accepting connections` and refuses to restart the WSGI server even though eventually postgres does finish starting up, django is stuck. in this event, wait and make sure that postgres has finished loading up (it will say `database system is ready to accept connections` in the postgres container logs) and then once you're sure, just kill and restart django via `docker kill DJANGO_CONTAINER_ID_GOES_HERE` and then `docker-compose up -d` again



how to run the tests
--------------------
- django's native testing is unittest
- to test the app go into django/web container via `docker exec -it CONTAINER_ID_GOES_HERE bash`
- do `python manage.py test web` and that will look for tests in the `web` django project and run them


