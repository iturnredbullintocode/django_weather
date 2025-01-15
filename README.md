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
- do `docker container inspect MEMCACHED_CONTAINER_ID_GOES_HERE` and toward the end it will show the specific ip address 
that is inside the docker container that it is running on - something like `192.168.48.2`
- take memcached's IP address and add it to the `.env.web-dev` file like `MEMCACHED_DOCKER_IP=192.168.48.2`

`python manage.py makemigrations` to make the migrations
`python manage.py migrate` to actually apply database changes


troubleshooting
------------------
- please note that I could automate and improve a lot of these issues but its out of the scope of a 4 hour project
- empty response could be because postgres stalled
    - sometimes, the postgres container takes a long time to load up
    - django gets an error like `django.db.utils.OperationalError: FATAL:  the database system is not yet accepting connections` 
    - it refuses to restart the WSGI server even though eventually postgres does finish starting up, django is stuck.
    - in this event, wait and make sure that postgres has finished loading up 
    - it will say `database system is ready to accept connections` in the postgres container logs
    - once you're sure, just kill and restart django via `docker kill DJANGO_CONTAINER_ID_GOES_HERE` and then `docker-compose up -d` again


how to run the tests
--------------------
- django's native testing is unittest
- to test the app go into django/web container via `docker exec -it CONTAINER_ID_GOES_HERE bash`
- do `python manage.py test web` and that will look for tests in the `web` django project and run them








caching

Memcached is an entirely memory-based cache server

Since version 3.2, Django has included a pymemcache-based cache backend.




django admin site
---------------------
- go into django/web container via `docker exec -it CONTAINER_ID_GOES_HERE bash`
- `python manage.py createsuperuser` fill in the info
    - `test_user`
    - Email address: `test_email@gmail.com`
    - pw `testtesttest`
- then go to `http://localhost:9100/admin/` and log in


django debug toolbar
----------------------
- django debug toolbar will let you track db queries if you need to.
- Go into django/web container via `docker exec -it CONTAINER_ID_GOES_HERE bash` 
- use `python manage.py debugsqlshell`
- models are currently commented out since they arent needed in this project but here are example queries:
    - `from polls.models import Choice, Question`
    - `Question.objects.all()`
    - `q = Question.objects.get(pk=1)`
    - `q.was_published_recently()`
- commands such as these will now show detailed sql queries that got ran behind the scenes







go into postgres/db container via `docker exec -it CONTAINER_ID_GOES_HERE bash`

and do `psql --username=USERNAME_GOES_HERE --dbname=DATABASE_NAME_GOES_HERE`
(so in our case `psql --username=test_user --dbname=django_test`) to go into database UI

do `\l` or `\list` to see list of databases

`\c django_test`  to change to the database

then do `\dt` to see tables in the database

you can `\q` to quit 