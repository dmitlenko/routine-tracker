# Makefile

This project uses a Makefile to simplify common development tasks. Here are the available commands:

## Setup and Installation

- `make install`: Sets up the project by creating a virtual environment, installing pre-commit hooks, and installing dependencies using Poetry.
- `make venv`: Creates a virtual environment if it doesn't exist.
- `make devenv`: Sets up a development environment by creating a virtual environment, installing dependencies, and copying a local settings file.

## Running the Application

- `make run`: Starts the development server.

## Database Operations

- `make migrate`: Applies database migrations.
- `make migrations`: Creates new database migrations.
- `make super`: Creates a superuser for the application.

## Development Tools

- `make shell`: Launches the Django shell.
- `make test`: Runs the project's test suite using pytest.
- `make lint`: Runs the flake8 linter on the project code.
- `make format`: Formats the project code using Black.

## Pre-commit Hooks

- `make install-pre-commit`: Installs pre-commit hooks.
- `make uninstall-pre-commit`: Uninstalls pre-commit hooks.
- `make pre-commit`: Runs all pre-commit hooks on all files.

## Docker

- `make docker-up-dev`: Starts the development server using Docker Compose.
- `make docker-build`: Builds the Docker image for the project.
- `make docker-down`: Stops the Docker containers.
