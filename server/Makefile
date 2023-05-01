export MONGO_URL?=mongodb://chat-mongodb:27017/chat-mongodb
export PYTHONPATH=$PYTHONPATH:./src

pytest:
	python -m pytest tests/

up:
	docker-compose up -d

down:
	docker-compose down --remove-orphans
