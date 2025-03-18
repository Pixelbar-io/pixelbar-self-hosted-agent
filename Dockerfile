FROM python:3.12-slim

WORKDIR /app

ARG GIT_HASH=unknown
ENV GIT_HASH=${GIT_HASH}

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh && \
    # Set ownership for application files
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose the port
EXPOSE 8000

# Run the application
CMD ["./entrypoint.sh"]
