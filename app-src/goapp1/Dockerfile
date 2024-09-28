# Start from the official Go image
FROM golang:1.23.1-alpine3.20 AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy go mod and sum files
COPY go.mod go.sum ./

# Download all dependencies
RUN go mod download

# Copy the source code into the container
COPY . .

# Build the application
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

FROM builder AS test
# Create a directory for test outputs
RUN mkdir -p /app/out

# copy the test.sh script
COPY test.sh /app/test.sh

# command to run the test.sh script
CMD ["/bin/sh", "/app/test.sh"]

# Start a new stage
FROM alpine:3.20.3 AS artifact

# Remove apk
RUN rm -rf /sbin/apk /etc/apk /lib/apk /usr/share/apk /var/lib/apk

# Create a non-root user and group
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Set the working directory
WORKDIR /app

# Copy the binary from the builder stage
COPY --from=builder /app/main .

# Change ownership of the application files
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Expose port 8080 to the outside world
EXPOSE 8080

# Command to run the executable
CMD ["./main"]