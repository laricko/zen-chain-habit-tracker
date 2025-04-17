psql:
	docker exec -it zen-chain-db psql -U postgres

# Example usage: make makemigrations message="create_table_name"
makemigrations:
	cd src/ && alembic -c app/alembic.ini revision --autogenerate -m $(message)

migrate:
	cd src/ && alembic -c app/alembic.ini upgrade head
