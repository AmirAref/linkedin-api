# pull base image
FROM python:3.11

WORKDIR /code/

RUN pip install uv

COPY requirements.lock ./
RUN uv pip install --no-cache --system -r requirements.lock

COPY . ./

# commands
# RUN alembic upgrade head
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--forwarded-allow-ips", "*"]
