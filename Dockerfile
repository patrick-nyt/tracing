FROM python:3.10

# Creating Application Source Code Directory
RUN mkdir -p /rolldice/src

# Setting Home Directory for containers
WORKDIR /rolldice/src

# Installing python dependencies
COPY requirements.txt /rolldice/src
RUN pip install --no-cache-dir -r requirements.txt

# Copying src code to Container
COPY . /rolldice/src

# Application Environment variables
ENV APP_ENV development

# Exposing Ports
EXPOSE 5000

#CMD opentelemetry-instrument --traces_exporter console  flask run app.py --host=0.0.0.0 --port=5000
# Running Python Application
CMD flask run --host=0.0.0.0 --port=5000
