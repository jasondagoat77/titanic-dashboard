FROM python:3.11-slim

WORKDIR /app

# Install system deps for matplotlib + wget for healthcheck
RUN apt-get update && apt-get install -y \
    libfreetype6-dev \
    libpng-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Pre-generate charts at build time
RUN python generate_charts.py

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "app:app"]