# Use the official Python Alpine image as a base image
FROM python:3.10-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SENTRY_DSN $FILM_JUNKIEZ_SENTRY_DSN

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Copy the application code
COPY . /app/

# Install build dependencies
RUN apk update && apk add --no-cache build-base libffi-dev openssl-dev postgresql-dev

# Upgrade pip and install required packages
RUN pip install --upgrade pip --no-cache-dir \
    && pip install -r requirements.txt \
    && pip install psycopg2-binary==2.9.9

# Copy the manage.py file
COPY ./manage.py /app/

# Run collectstatic (make sure manage.py is in /app/ directory)
RUN python manage.py collectstatic --noinput\
    && ls -l /app/

# Add a non-root user
RUN adduser -D myuser
#USER myuser

# Check file permissions and ownership
RUN chown -R myuser:myuser /app/staticfiles

# Expose the required ports
EXPOSE $PORT

# Use CMD to start the Gunicorn server
CMD gunicorn filmjunkiez.wsgi:application --bind 0.0.0.0:$PORT --reload --timeout 300 --log-level debug

