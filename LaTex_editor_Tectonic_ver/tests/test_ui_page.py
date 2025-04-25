import pytest
from backend.server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_ui_page_contains_form_and_fields(client):
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)

    assert "<form" in html, "No <form> tag found"

    assert "<textarea" in html, "No <textarea> tag found"

    assert "<button" in html or '<input type="submit"' in html, "No submit button found"

    assert 'type="file"' in html, "No file input field found"
