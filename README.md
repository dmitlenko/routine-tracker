# routine-tracker

## Project Description

This project is a simple routine tracker application that allows users to track their daily routines. Users can create routines, add tasks to routines, and mark tasks as completed.

## Requirements

- Python 3.12 or higher
- Poetry
- Docker and Docker Compose
- Linux or macOS

## Makefile Commands

This project uses a Makefile to simplify common development tasks. Here are the available commands:

### Setup and Installation

- `make install`: Sets up the project by creating a virtual environment, installing pre-commit hooks, and installing dependencies using Poetry.
- `make venv`: Creates a virtual environment if it doesn't exist.
- `make devenv`: Sets up a development environment by creating a virtual environment, installing dependencies, and copying a local settings file.

### Running the Application

- `make run`: Starts the development server.

### Database Operations

- `make migrate`: Applies database migrations.
- `make migrations`: Creates new database migrations.
- `make super`: Creates a superuser for the application.

### Development Tools

- `make shell`: Launches the Django shell.
- `make test`: Runs the project's test suite using pytest.
- `make lint`: Runs the flake8 linter on the project code.
- `make format`: Formats the project code using Black.

### Pre-commit Hooks

- `make install-pre-commit`: Installs pre-commit hooks.
- `make uninstall-pre-commit`: Uninstalls pre-commit hooks.
- `make pre-commit`: Runs all pre-commit hooks on all files.
