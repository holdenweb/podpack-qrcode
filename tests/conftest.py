"""Fixtures that build a real podpack site with this app installed."""

from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
from flask import Flask

from podpack import create_app

SiteFactory = Callable[..., Flask]

HOST_CONFIG: dict[str, Any] = {
    "site": {"name": "test site", "environment": "test", "apps": ["podpack_qrcode"]},
}


@pytest.fixture
def site(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> SiteFactory:
    monkeypatch.setenv("SECRET_KEY", "test-secret-key")
    monkeypatch.setenv("SQLALCHEMY_DATABASE_URI", "sqlite:///:memory:")

    def _build(**overrides: Any) -> Flask:
        config = {**HOST_CONFIG, **overrides.pop("host_config", {})}
        return create_app(
            host_config=config,
            data_root=tmp_path / "data",
            log_root=tmp_path / "logs",
            **overrides,
        )

    return _build


@pytest.fixture
def app(site: SiteFactory) -> Flask:
    """CSRF disabled so tests can POST without scraping a token; a separate
    test proves CSRF is on by default."""
    return site(config_overrides={"WTF_CSRF_ENABLED": False})
