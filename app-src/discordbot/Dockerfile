# Base Layer: Use an official Python Alpine image as a base
FROM python:3.11-alpine AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install build dependencies and general dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py main.py

# Test Layer: For running unit tests
FROM base AS test
ENV DISCORD_WEBHOOK_URL='https://discord.com/api/webhooks/test-url'

# Install additional dependencies required for testing
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

# Copy test-specific requirements and install them
COPY requirements-test.txt .
RUN pip install --no-cache-dir -r requirements-test.txt
COPY main_test.py ./
# Copy the test entrypoint script
COPY test.sh .

# Make the test script executable
RUN chmod +x test.sh

# Run tests
ENTRYPOINT ["./test.sh"]

# Artifact Layer: Clean layer with only necessary files
FROM python:3.11-alpine AS artifact

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a non-root user and group
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Set the working directory
WORKDIR /app

# Copy Python dependencies from the base layer
COPY --from=base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=base /usr/local/bin /usr/local/bin

# Remove unnecessary packages and clean up
RUN rm -rf /sbin/apk /etc/apk /lib/apk /usr/share/apk /var/lib/apk && \
    pip uninstall -y setuptools

# Copy the application code from the base layer
COPY --from=base /app /app

# Change ownership of the application files
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Command to run the application
CMD ["python", "main.py"]