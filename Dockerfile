# Use an official Python runtime as a parent image
FROM python:3.12.1-alpine3.19

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies required for Python packages
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev cargo
RUN pip install --upgrade pip && pip install setuptools wheel
RUN pip install -r requirements.txt
RUN apk del gcc musl-dev python3-dev libffi-dev openssl-dev cargo

# Create a non-root user and switch to it
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser
USER appuser

# Set the command to run the app
ENTRYPOINT ["python", "setup.py"]

