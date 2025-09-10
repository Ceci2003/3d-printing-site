#!/usr/bin/env bash
set -e

python manage.py migrate --noinput || true

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
python - <<'PY'
import os
from django.contrib.auth import get_user_model
os.environ.setdefault("DJANGO_SETTINGS_MODULE","app.settings")
import django; django.setup()
User = get_user_model()
u = os.environ["DJANGO_SUPERUSER_USERNAME"]
e = os.environ.get("DJANGO_SUPERUSER_EMAIL","")
p = os.environ["DJANGO_SUPERUSER_PASSWORD"]
if not User.objects.filter(username=u).exists():
    User.objects.create_superuser(u, e, p)
PY
fi

python manage.py collectstatic --noinput || true
exec gunicorn printing_site.wsgi:application --bind 0.0.0.0:8000 --workers 3
