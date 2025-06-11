#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

python manage.py init_site

python manage.py create_admin_user

if [[ $CREATE_SUPERUSER ]]
then
fi

