#!/bin/bash
python manage.py collectstatic

python manage.py runserver localhost:8100
