.PHONY: run build test lint clean coverage

# Default target
all: run

# Run the application locally
run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Build docker image
build:
	docker build -t pixelbar-agent:latest --build-arg GIT_HASH=$(git rev-parse --short HEAD) .

# Run the application in a Docker container
docker-run:
	docker run -p 8000:8000 --name pixelbar-agent pixelbar-agent

# Run tests
test:
	pytest

# Run tests with coverage
coverage:
	pytest --cov=app --cov-report=term --cov-report=html tests/

# Run linting
lint:
	flake8 app
	black --check app

# Format code
format:
	black app

# Clean up
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
