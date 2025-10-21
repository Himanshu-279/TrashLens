# Stage 1: Build stage
FROM python:3.10-slim as builder

WORKDIR /app

# System dependencies install karein
RUN apt-get update && apt-get install -y build-essential

# Requirements install karein
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Final stage
FROM python:3.10-slim

WORKDIR /app

# Builder stage se sirf zaroori wheels copy karein
COPY --from=builder /app/wheels /wheels/
RUN pip install --no-cache /wheels/*

# Baaki ka app code copy karein
COPY . .

# Ek naya user banayein (security ke liye)
RUN adduser --system --group appuser
RUN chown -R appuser:appuser /app
USER appuser

# build.sh script ko chalane ki ijaazat dein
RUN chmod +x ./build.sh

EXPOSE 7860

# Render ki persistent disk ke liye zaroori folders banayein
RUN mkdir -p /var/data/staticfiles

# Aakhri command, build script chalayega
CMD ["sh", "-c", "python manage.py migrate && gunicorn trashlens_project.wsgi --bind 0.0.0.0:7860"]