# podpack-qrcode

A podpack app that turns a piece of text into a QR code, delivered as a GIF.

The distribution is `podpack-qrcode`, the import name (for a site's `apps`
list) is `podpack_qrcode`, and the app answers to `qrcode` — its blueprint's
name, which keys `[site.mounts]` and its directories on disk.

## Routes

| Route | What it does |
| --- | --- |
| `/qrcode/` (GET) | the form |
| `/qrcode/` (POST) | the QR code, as `image/gif` |

## What it needs from the site

The form is CSRF-protected by flask-wtf, which uses the `SECRET_KEY` podpack
already requires — nothing to configure. There is no `[apps.qrcode]` section;
the app has no settings.
