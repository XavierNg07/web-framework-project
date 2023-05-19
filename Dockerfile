# pull official base image
FROM python:3.11.3-slim-buster

# set working directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# add app
COPY . /app

# start the application with a Gunicorn server
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]