# pull base image
FROM python:3.11

# Set Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Configure Poetry
ENV POETRY_VERSION=1.6.1
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_CACHE_DIR='/var/cache/pypoetry'
ENV POETRY_HOME='/usr/local'


WORKDIR /code/


# Install Poetry
# https://github.com/python-poetry/poetry
RUN curl -sSL 'https://install.python-poetry.org' | python - \
  && poetry --version


# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# install the dependencies
COPY poetry.lock pyproject.toml ./

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-dev --no-root ; fi"

COPY . ./

# commands
# RUN alembic upgrade head
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--forwarded-allow-ips", "*"]
