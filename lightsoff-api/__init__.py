import os
import sqlalchemy as sa
from typing import Optional
from flask_openapi3 import OpenAPI
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from pydantic import BaseModel, Field
from http import HTTPStatus

app = OpenAPI(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

CORS(app, origins=os.environ.get("CORS_ALLOWED_ORIGINS"))
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Place(db.Model):
    google_place_id = sa.Column(sa.Integer, primary_key=True, autoincrement=False)
    name = sa.Column(sa.Text, nullable=False)
    google_place_url = sa.Column(sa.Text)
    address = sa.Column(sa.Text, nullable=False)
    phone_number = sa.Column(sa.String(length=15))


class PlaceReview(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    google_place_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("place.google_place_id", name="place_review_place_fkey"),
        nullable=False,
    )
    created_at = sa.Column(sa.DateTime, nullable=False)
    completed_at = sa.Column(sa.DateTime)
    type = sa.Column(sa.String(50))
    do_it_for_me = sa.Column(sa.Boolean, default=False)


class PlaceBody(BaseModel):
    google_place_id: int
    name: str
    google_place_url: str
    address: str
    phone_number: Optional[str]

    class Config:
        orm_mode = True


class PlaceResponse(BaseModel):
    code: int = Field(0, description="Status Code")
    message: str = Field("ok", description="Exception Information")
    data: Optional[PlaceBody]


@app.post("/places", responses={"200": PlaceResponse})
def create_place(body: PlaceBody):
    place = (
        db.session.query(Place)
        .filter(Place.google_place_id == body.google_place_id)
        .first()
    )

    if not place:
        place = Place(**body.dict())
        db.session.add(place)
        db.session.commit()

    return {
        "message": "ok",
    }, HTTPStatus.OK


if __name__ == "__main__":
    app.run()
