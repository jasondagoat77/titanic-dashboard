FROM python:3.11-slim

WORKDIR /app

# Install system deps for matplotlib + wget for healthcheck using C libraries to render the images
RUN apt-get update && apt-get install -y \
    libfreetype6-dev \
    libpng-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Pre-generate charts at build time to reduce startup time
RUN python generate_charts.py

# waits for traffic to be routed to the container on port 5000
EXPOSE 5000

# Anyone can access the app on port 5000, and we use gunicorn to serve the app with 2 workers and a timeout of 120 seconds to handle longer requests if needed
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "app:app"]