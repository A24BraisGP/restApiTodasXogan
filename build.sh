#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
echo "---Execute collecstatic---" 
python manage.py collectstatic --no-input 

echo "---Execute migrate---"
python manage.py migrate

python manage.py init_site


