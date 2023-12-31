# Use the official Python Alpine image as a base image
FROM python:3.10-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SENTRY_DSN $FILM_JUNKIEZ_SENTRY_DSN

# Set the working directory
WORKDIR /filmjunkiez

# Copy the requirements file
COPY requirements.txt .

# Copy the manage.py file
COPY ./manage.py .


# Install build dependencies
RUN apk update && apk add --no-cache build-base libffi-dev openssl-dev postgresql-dev

# Upgrade pip and install required packages
RUN pip install --upgrade pip --no-cache-dir \
    && pip install -r requirements.txt \
    && pip install psycopg2-binary==2.9.9

# Copy the application code
COPY . .

# Run collectstatic
RUN python manage.py collectstatic --noinput\
    && ls -l /filmjunkiez/

# Add a non-root user
RUN adduser -D myuser
#USER myuser

# Check file permissions and ownership
RUN chown -R myuser:myuser /filmjunkiez/staticfiles

# Expose the required ports
EXPOSE ${PORT}

# Use CMD to start the Gunicorn server
CMD gunicorn filmjunkiez.wsgi:application --bind 0.0.0.0:${PORT} --reload --timeout 300 --log-level debug
