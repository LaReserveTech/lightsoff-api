# LightsOff API

## Built With

- [Python3](https://www.python.org/)
- [Poetry](https://python-poetry.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Docker](https://www.docker.com/) & [Docker Composer](https://docs.docker.com/compose/)

## Get Started

Copy environment file: `cp .env.template .env`

```console
make start
make run_migrations
```

Go to http://localhost:5000/openapi/

## Running tests

```console
make run_tests
```

## Generating a migration file

```console
make create_migration
```

## Deployment

This is handled by [Zappa](https://github.com/zappa/Zappa) in the `zappa.yml` github workflow
