# pull official base image
FROM python:3.11.3-slim-buster

# set working directory
WORKDIR /app

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# add app
COPY . .