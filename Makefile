# Makefile for routine_tracker

# Variables
PACKAGE_NAME = routine_tracker
POETRY_RUN = poetry run
MANAGE = $(POETRY_RUN) python -m $(PACKAGE_NAME).manage
LOCAL_SETTINGS = local/settings.dev.py

# Default target
.PHONY: install
install: venv
	$(POETRY_RUN) pre-commit install
	poetry install

.PHONY: run
run:
	$(MANAGE) runserver

.PHONY: test
test:
	$(MANAGE) test

.PHONY: migrate
migrate:
	$(MANAGE) migrate

.PHONY: migrations
migrations:
	$(MANAGE) makemigrations

.PHONY: shell
shell:
	$(MANAGE) shell

.PHONY: super
super:
	$(MANAGE) createsuperuser

.PHONY: secretkey
secretkey:
	$(MANAGE) generate_secret_key

# Create virtual environment
.PHONY: venv
venv:
	test -d venv || virtualenv venv

# Create a development environment
.PHONY: devenv
devenv: venv
	. venv/bin/activate; poetry install
	test $(LOCAL_SETTINGS) || cp $(PACKAGE_NAME)/project/settings/templates/settings.dev.py $(LOCAL_SETTINGS)

.PHONY: lint
lint:
	$(POETRY_RUN) flake8 $(PACKAGE_NAME)

.PHONY: format
format:
	$(POETRY_RUN) black $(PACKAGE_NAME)

# pre-commit hooks
.PHONY: install-pre-commit
install-pre-commit: uninstall-pre-commit
	$(POETRY_RUN) pre-commit install

.PHONY: uninstall-pre-commit
uninstall-pre-commit:
	$(POETRY_RUN) pre-commit uninstall

.PHONY: pre-commit
pre-commit:
	$(POETRY_RUN) pre-commit run --all-files


# translations
.PHONY: compile-translations
compile-translations: translations
	$(MANAGE) compilelocales

.PHONY: translations
translations:
	$(MANAGE) makelocales


# celery
.PHONY: celery
celery:
	celery -A routine_tracker.project worker --beat --scheduler django --loglevel=info


# docker
.PHONY: docker-up-dev
up-dev:
	docker-compose -f docker-compose.dev.yaml up

.PHONY: docker-build
build:
	docker-compose -f docker-compose.dev.yaml build

.PHONY: docker-down
down:
	docker-compose -f docker-compose.dev.yaml down
