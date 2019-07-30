DJANGO_CMD = python catalog/manage.py

SETTINGS = config.settings


clean:
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@find . -name ".cache" -type d | xargs rm -rf

conf-env:
	@cp -n contrib/localenv .env
	@echo 'Please configure params from .env file.'
	@read continue

migrations:
	$(DJANGO_CMD) makemigrations $(app)

migrate:
	$(DJANGO_CMD) migrate

requirements-pip:
	@pip install --upgrade pip
	@pip install -r requirements/development.txt

requirements-apt:
	@echo 'Root access required to install system dependencies from `requirements.apt` file'
	@sudo apt-get install $(shell cat requirements/ubuntu.apt | tr "\n" " ")


# Installation

createsuperuser:
	$(DJANGO_CMD) createsuperuser

install-backend-linux: requirements-apt requirements-pip migrate
	@echo "[OK] Backend dependencies installed"

install-linux: conf-env install-backend-linux createsuperuser
	@echo "[OK] Installation completed"

create_token:
	$(DJANGO_CMD) drf_create_token $(user)

# Tests

test: SHELL:=/bin/bash
test: clean
	export DEBUG=False && \
	export TEST=True && \
	export DATABASE_ENGINE=django.db.backends.sqlite3 && \
	export MYSQL_DATABASE_NAME=catalog_test.sqlite3 && \
	py.test catalog/ --ds=$(SETTINGS) -s

test-matching: SHELL:=/bin/bash
test-matching: clean
	export DEBUG=False && \
	export TEST=True && \
	export DATABASE_ENGINE=django.db.backends.sqlite3 && \
	export MYSQL_DATABASE_NAME=catalog_test.sqlite3 && \
	py.test catalog/ -k $(test) --ds=$(SETTINGS) -s


flake8:
	flake8 catalog/ --show-source --exclude=wsgi.py,manage.py,*migration*

# Development

shell: clean
	$(DJANGO_CMD) shell

runserver: clean
	$(DJANGO_CMD) runserver 0.0.0.0:8000
