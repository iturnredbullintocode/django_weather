# syntax=docker/dockerfile:1

# start with the python 3.8.5 docker image, as the OS on docker
FROM python:3.8.5

# set environment variables
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr 
ENV PYTHONUNBUFFERED=1

# make a directory on the docker filesystem called "/usr/src/app"
RUN mkdir -p /usr/src/app
# CD into the "/usr/src/app" directory in the docker filesystem
WORKDIR /usr/src/app

# copy "requirements.txt" from the local filesystem,
# into "/user/src/app" folder in the docker filesystem
COPY requirements.txt /usr/src/app/
# make pip install all the requirements in this file, onto the docker filesystem
RUN pip install --no-cache-dir -r requirements.txt

# copy everything in the "." folder on the local filesystem
# ("." refers to the current folder we're in, the "web" folder)
# into the specified "user/src/app" folder in the docker filesystem
# (the leading '/' specifies the root folder)
COPY . /usr/src/app
