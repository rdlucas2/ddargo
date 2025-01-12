# Stage 1: Base - Build the Python environment and install dependencies
FROM python:3.11-alpine AS base

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY main.py ./

# Stage 2: Test - Run tests (assuming a test script is available)
FROM base AS test
COPY requirements-test.txt ./
RUN pip install --no-cache-dir -r requirements-test.txt
COPY main_test.py ./
COPY test.sh ./

# Create a directory for test outputs
RUN mkdir -p /app/out

# Command to run the test script
CMD ["/bin/sh", "/app/test.sh"]

# Stage 3: Artifact - Create the final production image
FROM python:3.11-alpine AS artifact

# Create a non-root user and group
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Set the working directory
WORKDIR /app

# Copy the Python environment (including uvicorn and other installed packages) from the base stage
COPY --from=base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=base /usr/local/bin /usr/local/bin

# Remove unnecessary packages and clean up
RUN rm -rf /sbin/apk /etc/apk /lib/apk /usr/share/apk /var/lib/apk && \
    pip uninstall -y setuptools

# Copy the application files from the build stage
COPY --from=base /app /app

# Change ownership of the application files
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
