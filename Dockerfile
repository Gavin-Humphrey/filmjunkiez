FROM python:3.9-alpine


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SENTRY_DSN $SENTRY_DSN

WORKDIR /code

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir

RUN pip install -r requirements.txt


COPY . /code/

RUN python manage.py collectstatic --noinput

# add and run as non-root user
RUN adduser -D myuser
USER myuser

# Expose the required ports
EXPOSE $PORT

# Start Gunicorn or the Django server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:$PORT"]

CMD gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:$PORT