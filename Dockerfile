# this is an official Python runtime, used as the parent image
FROM python:3.7-slim

# set the working directory in the container to /app
WORKDIR /app

# add the current directory to the container as /app
ADD ./requirements.txt /app/requirements.txt

# execute everyone's favorite pip command, pip install -r
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# add the current directory to the container as /app
ADD . /app

# unblock port 80 for the Flask app to run on
EXPOSE 5000

# execute the Flask app
ENTRYPOINT ["python", "app.py"]
