.PHONY: start stop clean run_migrations create_migration run_tests

start:
	@docker compose up --build --detach --remove-orphans

stop:
	@docker compose stop

watch:
	@docker compose logs --tail 100 --follow

clean:
	@docker compose stop
	@docker compose rm --volumes --force

run_migrations:
	@docker compose run -d database
	@docker compose run --rm --entrypoint '' api flask db upgrade

create_migration: run_migrations
	@docker compose run --rm --entrypoint '' api flask db migrate -m "Reword me"

run_tests:
	@docker compose run -d database
	@docker compose run -e DATABASE_NAME=lightsoff_test --rm --entrypoint '' api pytest
