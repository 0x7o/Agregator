python3 manage.py makemigrations
python3 manage.py migrate
gunicorn api.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:80 --reload --workers 5 --timeout 120