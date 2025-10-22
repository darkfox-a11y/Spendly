# =======================================
# Spendly Backend - Secure Dockerfile
# =======================================

# Base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Disable Python buffering for better logging
ENV PYTHONUNBUFFERED=1

# Copy dependency list first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the project files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Default startup command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
