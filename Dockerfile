FROM python:3.10-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SENTRY_DSN $FILM_JUNKIEZ_SENTRY_DSN

# Set the working directory
WORKDIR /app 

RUN adduser -D app

RUN adduser app wheel

# Copy the requirements file
COPY requirements.txt .

# Copy the manage.py file
COPY ./manage.py .

# Install build dependencies
RUN apk update && apk add --no-cache build-base libffi-dev openssl-dev postgresql-dev

RUN pip install setuptools

#Upgrade pip and install required packages
RUN pip install --upgrade pip --no-cache-dir \
    && pip install -r requirements.txt \
    && pip install psycopg2-binary==2.9.9 

ENV PATH="/py/bin:$PATH" 

# Copy the application code
COPY . .

# Run collectstatic
RUN python manage.py collectstatic --noinput

# Add a non-root user
#RUN adduser -D myuser

# Grant write access to the media and staticfiles directories
RUN chmod -R 777 /app/media /app/staticfiles

# Expose the required ports
EXPOSE ${PORT}

# Use CMD to start the Gunicorn server
CMD gunicorn filmjunkiez.wsgi:application --bind 0.0.0.0:${PORT} --timeout 300 --log-level debug
 