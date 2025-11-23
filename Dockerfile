# Use the official Python base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Set environment variable for port
ENV PORT 8080

# Expose the port (Gunicorn will run on this port)
EXPOSE 8080

# Run the application using Gunicorn (from your Procfile)
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--timeout", "120"]