up:
	docker-compose up -d 

up-build:
	docker-compose up -d --build

kill:
	docker-compose kill

test:
	docker-compose exec backend pytest .

lint: 
	docker-compose exec backend black .
	docker-compose exec backend flake8 .
	docker-compose exec backend isort .

logs-backend:
	docker-compose logs backend

logs-frontend:
	docker-compose logs frontend

ps:
	docker-compose ps