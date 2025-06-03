# Dockerfile pentru rularea auditului static

FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "audit_en_full.py", "."]
