# Use official Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install build dependencies for any packages if needed (optional)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . .

# Expose the port Gunicorn will listen on
EXPOSE 5000

RUN apt install -y curl

# Use Gunicorn as production server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--workers", "3", "--threads", "2", "--timeout", "120"]
