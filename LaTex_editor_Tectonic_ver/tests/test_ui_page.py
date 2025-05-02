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


def test_full_tectonic_ui_elements(client):
    resp = client.get('/')
    html = resp.get_data(as_text=True)

    assert 'id="main"' in html
    assert 'id="editor"' in html
    assert 'id="preview"' in html
    assert 'id="writepad"' in html

    assert "<h3>Code</h3>" in html
    assert "<h3>Review</h3>" in html

    assert '>Render<' in html
    assert '>Copy LaTeX<' in html
    assert '>Download PDF<' in html

    assert 'id="latexInput"' in html
    assert 'id="renderOutput"' in html
    assert 'id="uploadForm"' in html

    assert 'latex.min.js' in html
