from lightsoff_api import db, Place, PlaceReview


def test_post_place_reveiw(client):
    existing_place = Place(
        report_count=8,
        google_place_id="some_id",
        name="some_name",
        address="some_address",
    )
    db.session.add(existing_place)

    review_payload = {
        "type": "PHONE_CALL",
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
