
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x ./build.sh

EXPOSE 10000

CMD ["sh", "-c", "./build.sh && python manage.py migrate && gunicorn trashlens_project.wsgi --bind 0.0.0.0:10000"]

#CMD ["sh", "-c", "./build.sh && python manage.py migrate && gunicorn trashlens_project.wsgi --bind 0.0.0.0:10000 --workers 1 --threads 1 --timeout 120"]
