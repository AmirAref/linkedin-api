# pull base image
FROM python:3.10

# Set Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Dependencies
COPY Pipfile Pipfile.lock /code/
WORKDIR /code
RUN pip install pipenv && pipenv install --system
# copy Project
COPY . /code/

# commands
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]