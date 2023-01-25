.PHONY: all install update uninstall

all:
	@docker compose run --rm --entrypoint '' api flask db upgrade

install:
	@docker compose up --detach --remove-orphans

update:
	@docker compose pull
	@docker compose up --force-recreate --build --detach

uninstall:
	@docker compose stop
	@docker compose rm --volumes --force
