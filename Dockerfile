# this is an official Python runtime, used as the parent image
FROM python:3.7-slim

# set the working directory in the container to /app
WORKDIR /srv/flask_app

RUN apt-get clean \
    && apt-get -y update
RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential

# add the current directory to the container as /app
ADD ./requirements.txt ./requirements.txt

# execute everyone's favorite pip command, pip install -r
RUN pip install --trusted-host pypi.python.org -r requirements.txt --src /usr/local/src

# add the current directory to the container
COPY . /srv/flask_app

# unblock port 80 for the Flask app to run on
EXPOSE 80

# copy the nginx config, chmod the startup script, and set the startup
COPY nginx.conf /etc/nginx
RUN chmod +x ./start.sh
CMD ["./start.sh"]
