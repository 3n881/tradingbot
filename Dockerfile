# # Base image
# FROM python:3.10-slim

# # Set the working directory
# WORKDIR /app

# # Copy requirements
# COPY requirements.txt .

# # Install dependencies with increased timeout
# RUN pip install --no-cache-dir --default-timeout=120 -r requirements.txt

# # Copy application code
# COPY . .

# # Expose application port
# EXPOSE 8000

# # Command to run the application
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# Base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy pre-downloaded Python packages into the container
# COPY ./packages /packages
COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --upgrade pip setuptools


# Install the pre-downloaded dependencies
# RUN pip install --no-cache-dir /packages/*
RUN pip install -r requirements.txt



# Copy the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

