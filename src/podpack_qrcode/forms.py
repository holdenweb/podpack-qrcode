from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class QRCodeForm(FlaskForm):
    qrcode_text = StringField("qrcode_text")
    submit = SubmitField("Get QR Code")
