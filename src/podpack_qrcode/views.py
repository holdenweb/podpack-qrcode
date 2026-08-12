"""One form, one image: the QR code generator."""

import io
from logging import getLogger

import qrcode
from flask import Blueprint, Response, render_template, request
from flask.typing import ResponseReturnValue
from qrcode.image.pil import PilImage

from .forms import QRCodeForm

logger = getLogger(__name__)

blueprint = Blueprint("qrcode", __name__, template_folder="templates")


@blueprint.route("/", methods=["GET", "POST"])
def form() -> ResponseReturnValue:
    form = QRCodeForm()
    if form.validate_on_submit():
        text = request.form["qrcode_text"]
        # The PIL factory named explicitly: qrcode falls back to a PyPNG-backed
        # image without Pillow, whose save() cannot produce the GIF promised.
        image = qrcode.make(text, image_factory=PilImage)
        memfile = io.BytesIO()
        image.save(memfile, format="GIF")
        logger.info("generated a QR code of %d characters", len(text))
        return Response(memfile.getvalue(), mimetype="image/gif")
    return render_template("qrcode/form.html", form=form, title="QR Code Generator")
