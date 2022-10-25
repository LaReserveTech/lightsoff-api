# Development setup

- [Install poetry](https://python-poetry.org/docs/#installation)
- Install python 3.9
- Create a virtual `python -m venv venv`
- Activate `source venv/bin/activate`
- Install dependencies `poetry install`
- Copy environment file: `cp .env.template .env`
- Replace environment variables with yours
- Run migrations `flask db upgrade`
- Launch the app `flask run`
