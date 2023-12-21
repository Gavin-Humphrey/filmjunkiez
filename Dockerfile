# Build Level
FROM python:3.10-alpine AS builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt .

# Install build dependencies
RUN apk add --no-cache build-base libffi-dev openssl-dev && \
    apk add --no-cache postgresql-dev

# Install Python dependencies
RUN pip install --no-build-isolation --ignore-installed -r requirements.txt && \
    pip install psycopg2-binary==2.9.9


# Runtime Level
FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SENTRY_DSN $FILM_JUNKIEZ_SENTRY_DSN

WORKDIR /code

# Install the PostgreSQL client library
RUN apk add --no-cache postgresql-libs

# Copy only the necessary files from the builder stage
COPY --from=builder /code /code
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

RUN adduser -D myuser
USER myuser

EXPOSE $PORT

# Use CMD to start the Gunicorn server
CMD gunicorn filmjunkiez.wsgi:application --bind 0.0.0.0:$PORT
