"""Conformance with the podpack app contract, and the QR codes themselves."""

from flask import Flask

from conftest import SiteFactory

from podpack_qrcode import site_app


def test_the_app_names_itself_after_its_blueprint() -> None:
    assert site_app.name == site_app.blueprint.name == "qrcode"


def test_a_site_installs_it_by_naming_it(site: SiteFactory) -> None:
    app = site()
    assert app.test_client().get("/qrcode/").status_code == 200
    assert app.extensions["podpack"].installed_from == {"qrcode": "podpack_qrcode"}


def test_the_site_decides_where_it_lands(site: SiteFactory) -> None:
    app = site(
        host_config={
            "site": {
                "name": "test site",
                "environment": "test",
                "apps": ["podpack_qrcode"],
                "mounts": {"qrcode": "/tools/qr"},
            }
        }
    )
    client = app.test_client()
    assert client.get("/tools/qr/").status_code == 200
    assert client.get("/qrcode/").status_code == 404


def test_the_form_renders(app: Flask) -> None:
    body = app.test_client().get("/qrcode/").get_data(as_text=True)
    assert "QR Code Generator" in body
    assert 'name="qrcode_text"' in body


def test_a_post_returns_a_gif(app: Flask) -> None:
    response = app.test_client().post(
        "/qrcode/", data={"qrcode_text": "https://holdenweb.com/"}
    )
    assert response.status_code == 200
    assert response.mimetype == "image/gif"
    assert response.data.startswith(b"GIF8")


def test_csrf_protects_the_form_by_default(site: SiteFactory) -> None:
    """The site's SECRET_KEY is all flask-wtf needs; no app configuration."""
    app = site()
    response = app.test_client().post("/qrcode/", data={"qrcode_text": "x"})
    # A tokenless POST falls through to re-rendering the form, not to an image.
    assert response.mimetype == "text/html"
