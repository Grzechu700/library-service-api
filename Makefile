.PHONY: help build up down restart logs shell migrate test clean

help:
	@echo "Available commands:"
	@echo "  make build     - Build Docker images"
	@echo "  make up        - Start all services"
	@echo "  make down      - Stop all services"
	@echo "  make restart   - Restart all services"
	@echo "  make logs      - Show logs"
	@echo "  make shell     - Open Django shell"
	@echo "  make migrate   - Run migrations"
	@echo "  make test      - Run tests"
	@echo "  make clean     - Remove containers and volumes"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

shell:
	docker-compose exec web python manage.py shell

migrate:
	docker-compose exec web python manage.py migrate

test:
	docker-compose exec web pytest

clean:
	docker-compose down -v
	docker system prune -f
