FROM python:3.9

WORKDIR /app

RUN python -m pip install --upgrade pip
RUN pip install gunicorn

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

# RUN python manage.py makemigrations
# RUN python manage.py migrate
# RUN python manage.py collectstatic
# RUN cp -r /app/collected_static/. /backend_static/static/

CMD ["gunicorn", "backend.wsgi", "--bind", "0:9000"]
