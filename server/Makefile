export MONGO_URI?=mongodb://chat-mongodb:27017/chat-mongodb
export PYTHONPATH=$PYTHONPATH:./src

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

pytest:
	python -m pytest tests/

up:
	docker-compose up -d

down:
	docker-compose down --remove-orphans
