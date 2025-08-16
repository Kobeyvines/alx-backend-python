# Use official Python image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    && apt-get clean && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Expose Django default port
EXPOSE 8000

# Run Django server
# Run with: docker run -p 8000:8000 messaging_app_image
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
