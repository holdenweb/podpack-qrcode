"""The qrcode app: turn a piece of text into a QR code image."""

from podpack import Section, SiteApp

from .views import blueprint

site_app = SiteApp(
    blueprint=blueprint,
    url_prefix="/qrcode",
    # `qrcode.form`, not `podpack_qrcode.form`: nav names an *endpoint*, and
    # endpoints carry the blueprint's name, which is this app's name (ADR-0003).
    # `podpack_qrcode` is only the import name -- what a site's `apps` list
    # carries -- and the two differ deliberately.
    nav=(Section("QR codes", "qrcode.form"),),
)
