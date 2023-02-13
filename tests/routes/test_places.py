from lightsoff_api import db, Place


def test_post_new_place(client):
    place_payload = {
        "google_place_id": "Some id",
        "name": "Some name",
        "google_place_url": "Some URL",
        "address": "Some address",
        "phone_number": "Some number",
        "latitude": 0.1,
        "longitude": 0.2,
        "contacted": 0,
    }

    response = client.post(
        "/places",
        json=place_payload,
    )

    assert response.status_code == 200

    place = db.session.query(Place).filter(Place.google_place_id == "Some id").one()

    for key, value in place_payload.items():
        assert getattr(place, key) == value

    assert place.report_count == 1


def test_post_existing_place(client):
    place_payload = {
        "google_place_id": "Some id",
        "name": "Some name",
        "google_place_url": "Some URL",
        "address": "Some address",
        "phone_number": "Some number",
        "latitude": 0.1,
        "longitude": 0.2,
        "contacted": 0
    }

    existing_place = Place(report_count=8, **place_payload)
    db.session.add(existing_place)

    response = client.post(
        "/places",
        json=place_payload,
    )

    assert response.status_code == 200

    for key, value in place_payload.items():
        assert getattr(existing_place, key) == value

    assert existing_place.report_count == 9
