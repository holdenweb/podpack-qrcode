"""The qrcode app: turn a piece of text into a QR code image."""

from podpack import SiteApp

from .views import blueprint

site_app = SiteApp(
    blueprint=blueprint,
    url_prefix="/qrcode",
    Section("QR Code", "podpack_qrcode.form"),
)
