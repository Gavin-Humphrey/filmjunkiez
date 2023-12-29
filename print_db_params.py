# print_db_params.py
import os
from django import setup
from django.conf import settings

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'filmjunkiez.settings')
setup()
print(os.environ)
# Print all database connection parameters
for alias in settings.DATABASES:
    connection_params = settings.DATABASES[alias]
    print(f'--- {alias} ---')
    for key, value in connection_params.items():
        print(f'{key}: {value}')
