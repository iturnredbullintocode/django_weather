Dockerized weather app
=====================
Django - Postgres - Memcached


running the app
--------------------
- Don't use any of these variables/settings in production, for the sake of speed most of them are sitting in the .env file, and the file is being git tracked.
- Ask me for the weather api key, or use your own - open `.env.web-dev` file set `WEATHER_API_KEY=` (add the key right after the `=` sign)
    - You could also get your own API key by signing up for the weather API used in the app at https://www.weatherapi.com/
- Assuming development environment will be needed friday, so django toolbar is currently set to on, as well, and project settings are dev mode.
- you will need Docker installed to run the app
- simply clone the entire repo and `docker-compose build` and `docker-compose up -d`
- the app won't be ready yet because the containers need adjustments:
    - do `docker ps` and grab the container id of the django container
    - execute a database migration command inside the django container via `docker exec -it DJANGO_CONTAINER_ID_GOES_HERE python manage.py migrate`
    - do `docker ps` and grab the container id of the memcached container
    - do `docker container inspect MEMCACHED_CONTAINER_ID_GOES_HERE` and toward the end it will show the specific ip address 
        that is inside the docker container that it is running on - something like `192.168.48.2`
    - take memcached's IP address and add it to the `.env.web-dev` file like `MEMCACHED_DOCKER_IP=192.168.48.2`
- now you will need to kill and restart the django container via `docker kill DJANGO_CONTAINER_ID_GOES_HERE` and then `docker-compose up -d` again
- three docker containers will spin up:
    - django on http://localhost:9100
    - postgres on http://localhost:9200
    - memcached server on http://localhost:9300

- **Now, the app should be ready you can start using the app right away in your browser
   on `http://localhost:9100` it will show the homepage and you can try inputting data**



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





why memcache?
-----
Memcached is an entirely memory-based cache server.
More lightweight than redis, but still one of the fastest caching solutions around.
The pymemcache library that is used in this project was developed by pinterest
and since version 3.2, Django has included a pymemcache-based cache backend.



validation
----------
django's built-in forms/modelforms/models have fantastic validators for fields, and they're very nicely extendable, all you need


front end
------
just templates, for the sake of speed. I did make the app send subtemplates via ajax though, 
for the sake of good user experience with error-handling,
not having to wait if the api times out for some reason, more natural feel




considerations (not implemented)
---------------------------------
- IP address based throttling should be implemented
    - although the cache is nice, a user could just spam the API with a crapton of different zipcodes and
        abuse my API key so additional ways to throttle requests would be ice
- logging could be done better, I just threw in a logging library with random logs for a few things, ran out of time
- fetch_weather should be rewritten as a method of the weather class,
    - split into multiple methods one for cache, one for api
    - more intuitive to have it all in one class
- pymemcache error handling should be added, here is list of all possible errors
    - pymemcache.exceptions.MemcacheUnknownCommandError
    - pymemcache.exceptions.MemcacheClientError
    - pymemcache.exceptions.MemcacheServerError
    - pymemcache.exceptions.MemcacheUnknownError
    - pymemcache.exceptions.MemcacheUnexpectedCloseError
    - pymemcache.exceptions.MemcacheIllegalInputError
    - socket.timeout
    - socket.error
- ajax 500 error and other server error wrapping
    - ajax function should be as simple as possible - just return subtemplate
    - this means that 500, 404 errors and other page errors should be handled
        in a specific way by *django*, for ajax requests, not by front end or template
    - preferably with a wapper such as @ajax (I think one exists, but needs
        to be extended to handle server errors)



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



postgres
----
technically, the DB is not in use because we only need to store key value pairs to
prevent the api being hit too often, and for that, a cache is more efficient.
however, I am assuming y'all will ask me to add more data or some sort of interactions,
so I've set up appropriate database models ahead of time but commented them out for now.

postgres can be connected to if you have pgadmin
- Host name/address: `localhost`
- Port: `9200`
- Username: `test_user` 
- Password: `test_password`

you can go into postgres/db container via `docker exec -it CONTAINER_ID_GOES_HERE bash`
- do `psql --username=test_user --dbname=django_test` to go into database UI
- do `\l` or `\list` to see list of databases
- `\c django_test`  to change to the database
- then do `\dt` to see tables in the database
- you can `\q` to quit 