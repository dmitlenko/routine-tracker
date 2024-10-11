# Makefile for routine_tracker

# Variables
PACKAGE_NAME = routine_tracker
POETRY_RUN = poetry run
MANAGE = $(POETRY_RUN) python -m $(PACKAGE_NAME).manage
LOCAL_SETTINGS = local/settings.dev.py

# Default target
.PHONY: install
install: venv
	poetry install

.PHONY: run
run:
	$(MANAGE) runserver

.PHONY: test
test:
	$(POETRY_RUN) pytest

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

# Create virtual environment
.PHONY: venv
venv:
	test -d venv || virtualenv venv

# Create a development environment
.PHONY: devenv
devenv: venv
# Create a virtual environment
	. venv/bin/activate; poetry install
	test $(LOCAL_SETTINGS) || cp $(PACKAGE_NAME)/project/settings/templates/settings.dev.py $(LOCAL_SETTINGS)
