from lightsoff_api import db, Place, PlaceReview
import datetime


def test_post_place_review_with_type(client):
    existing_place = Place(
        report_count=8,
        google_place_id="some_id",
        name="some_name",
        address="some_address",
        latitude=0.1,
        longitude=0.1,
    )
    db.session.add(existing_place)

    review_payload = {
        "type": "GOOGLE_REVIEW",
        "do_it_for_me": False,
    }

    response = client.post(
        f"/places/{existing_place.google_place_id}/reviews",
        json=review_payload,
    )

    assert response.status_code == 200

    place_review = (
        db.session.query(PlaceReview)
        .filter(PlaceReview.google_place_id == existing_place.google_place_id)
        .one()
    )

    for key, value in review_payload.items():
        assert getattr(place_review, key) == value


def test_post_place_review_with_wrong_payload(client):
    existing_place = Place(
        report_count=8,
        google_place_id="some_id",
        name="some_name",
        address="some_address",
        latitude=0.1,
        longitude=0.1,
    )
    db.session.add(existing_place)

    response = client.post(
        f"/places/{existing_place.google_place_id}/reviews",
        json={
            "type": None,
            "do_it_for_me": None,
        },
    )

    assert response.status_code == 422
    assert response.json[0]["msg"] == "type or do_it_for_me fields should not be null"

    response = client.post(
        f"/places/{existing_place.google_place_id}/reviews",
        json={
            "type": "GOOGLE_REVIEW",
            "do_it_for_me": True,
        },
    )

    assert response.status_code == 422
    assert response.json[0]["msg"] == "type or do_it_for_me fields should be null"

    response = client.post(
        f"/places/{existing_place.google_place_id}/reviews",
        json={
            "type": None,
            "do_it_for_me": False,
        },
    )

    assert response.status_code == 422
    assert response.json[0]["msg"] == "type field should not be null"

    response = client.post(
        f"/places/{existing_place.google_place_id}/reviews",
        json={
            "type": "YOLO",
            "do_it_for_me": False,
        },
    )

    assert response.status_code == 422
    assert "value is not a valid enumeration member" in response.json[0]["msg"]


def test_delete_place_review(client):
    existing_place = Place(
        report_count=8,
        google_place_id="some_id",
        name="some_name",
        address="some_address",
        latitude=0.1,
        longitude=0.1,
    )
    db.session.add(existing_place)

    existing_place_review = PlaceReview(
        id=12,
        google_place_id="some_id",
        created_at=datetime.datetime.utcnow(),
        completed_at=datetime.datetime.utcnow(),
        type="GOOGLE_REVIEW",
        do_it_for_me=False,
    )
    db.session.add(existing_place_review)

    delete_review_payload = {
        "id": existing_place_review.id
    }

    response = client.delete(
        f"/place_reviews",
        json=delete_review_payload,
    )

    assert response.status_code == 200

    place_review = (
        db.session.query(PlaceReview)
        .filter(PlaceReview.id == existing_place_review.id)
        .all()
    )

    assert place_review == []


def test_delete_place_review_when_the_id_does_not_exist(client):

    delete_review_payload = {
        "id": 999
    }

    response = client.delete(
        f"/place_reviews",
        json=delete_review_payload,
    )

    assert response.status_code == 204
