import os
import sqlalchemy as sa
import datetime
from typing import Optional
from flask_openapi3 import OpenAPI
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from pydantic import BaseModel, Field
from http import HTTPStatus

app = OpenAPI(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

CORS(app, origins=os.environ.get("CORS_ALLOWED_ORIGINS", "").split(","))
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Place(db.Model):
    google_place_id = sa.Column(sa.Text, primary_key=True, autoincrement=False)
    name = sa.Column(sa.Text, nullable=False)
    created_at = sa.Column(sa.DateTime, nullable=False)
    address = sa.Column(sa.Text, nullable=False)
    google_place_url = sa.Column(sa.Text)
    phone_number = sa.Column(sa.String(length=15))
    report_count = sa.Column(sa.Integer, nullable=False, default=1)


class PlaceReview(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    google_place_id = sa.Column(
        sa.Text,
        sa.ForeignKey("place.google_place_id", name="place_review_place_fkey"),
        nullable=False,
    )
    created_at = sa.Column(sa.DateTime, nullable=False)
    completed_at = sa.Column(sa.DateTime)
    type = sa.Column(sa.String(50))
    do_it_for_me = sa.Column(sa.Boolean, default=False)


class PlacePath(BaseModel):
    google_place_id: str


class PlaceBody(BaseModel):
    google_place_id: str
    name: str
    google_place_url: str
    address: str
    phone_number: Optional[str]

    class Config:
        orm_mode = True


class PlaceResponse(BaseModel):
    code: int = Field(0, description="Status Code")
    message: str = Field("ok", description="Exception Information")


@app.post("/places", responses={"200": PlaceResponse})
def create_place(body: PlaceBody):
    place = (
        db.session.query(Place)
        .filter(Place.google_place_id == body.google_place_id)
        .first()
    )

    if not place:
        db.session.add(Place(created_at=datetime.datetime.utcnow(), **body.dict()))
    else:
        place.report_count += 1

    db.session.commit()

    return {
        "code": HTTPStatus.OK.value,
        "message": HTTPStatus.OK.description,
    }, HTTPStatus.OK


class PlaceReviewBody(BaseModel):
    type: Optional[str]
    do_it_for_me: Optional[bool]

    class Config:
        orm_mode = True


class PlaceReviewResponse(BaseModel):
    code: int = Field(0, description="Status Code")
    message: str = Field("ok", description="Exception Information")


@app.post(
    "/places/<string:google_place_id>/reviews", responses={"200": PlaceReviewResponse}
)
def create_place_review(path: PlacePath, body: PlaceReviewBody):
    place = (
        db.session.query(Place)
        .filter(Place.google_place_id == path.google_place_id)
        .first()
    )

    if not place:
        return {
            "code": HTTPStatus.NOT_FOUND.value,
            "message": HTTPStatus.NOT_FOUND.description,
        }, HTTPStatus.NOT_FOUND

    place_review = PlaceReview(
        google_place_id=place.google_place_id,
        created_at=datetime.datetime.utcnow(),
        completed_at=datetime.datetime.utcnow() if not body.do_it_for_me else None,
        **body.dict(),
    )
    db.session.add(place_review)
    db.session.commit()

    return {
        "code": HTTPStatus.OK.value,
        "message": HTTPStatus.OK.description,
    }, HTTPStatus.OK


if __name__ == "__main__":
    app.run()
