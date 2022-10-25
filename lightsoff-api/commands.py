import flask_migrate
from . import app


def upgrade():
    with app.app_context():
        flask_migrate.upgrade()
