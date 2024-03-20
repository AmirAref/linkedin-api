# Linkedin API
a web API service to get this is a tool to download the videos, pictures, documents, etc of a [Linkedin.com](https://linkedin.com) post developed by **FastAPI**.


<br>

## Documentation
the API documentations are <a href="https://linkedin.iran.liara.run/docs" target="_blank">here</a>.  
  
<br>

## Usage
this project is now deployed <a href="https://linkedin.iran.liara.run" target="_blank">here</a> that you can use it free and easily.
if you are a developer or you want to get data by the API go to the <a href="#documentation" target="_blank">Documentation</a>

<br>

## Install & Run :
also if you want to host this project on your own server or your machine, just clone the project on your machine and then choose one of the following options:

### 1. Docker
to run with docker you have to install the docker in your machine and then run the following command (in the project directory) :
```bash
docker build . -t linkedinapi
docker run -p "80:8000" linkedinapi
```
_you can also run in detached mode with `docker run -d`_

<br>

### 2. Manually Install:
to install and run the project manually follow these steps in the bash terminal (in the project directory) :  
_**NOTICE**_ : you have to install python version `3.10` or higher on your machine.
```bash
# install the dependencies
pip install pipenv && pipenv install
# go to pipenv shell
pipenv shell
# run the app using uvicorn webserver
uvicorn src.main:app --host 0.0.0.0
```
