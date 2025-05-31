migrate:
	alembic upgrade head

seed:
	python scripts/seed_data.py

test:
	bash scripts/run_tests.sh

lint:
	flake8 src tests
	mypy src

format:
	black src tests
	isort src tests

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .coverage htmlcov/ .pytest_cache/ .mypy_cache/

run-dev:
	python scripts/run_dev.py

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

# Full setup for new development environment
setup: install-dev docker-up setup-db migrate seed
	@echo "Development environment ready!"
	@echo "Run 'make run-dev' to start the server"