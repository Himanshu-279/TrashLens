# Koi fancy logic nahi, sab kuch ek hi baar mein
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Pehle saare system tools install karo
RUN apt-get update && apt-get install -y --no-install-recommends build-essential

# Ab saare python packages install karo
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Aakhir mein, poora code copy karo
COPY . .

EXPOSE 10000 # Render 10000 port ka istemal karta hai

# YEH HAI ASLI JAADU - AAKHRI COMMAND
# Yeh saari commands tab chalengi jab app LIVE hoga, jahan /var/data maujood hai
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn trashlens_project.wsgi --bind 0.0.0.0:10000"]