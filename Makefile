PYTHON ?= uv run python

.PHONY: dev dev-backend dev-frontend build deploy

dev:
	$(PYTHON) manage.py runserver & cd frontend && npm run dev

dev-backend:
	$(PYTHON) manage.py runserver

dev-frontend:
	cd frontend && npm run dev

build:
	cd frontend && npm run build

deploy: build
	$(PYTHON) manage.py collectstatic --noinput
